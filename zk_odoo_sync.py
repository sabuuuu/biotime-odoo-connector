"""ZKBioTime to Odoo (hr.attendance) synchronization logic.

One hr.attendance record per employee and per day, rebuilt on every run from all the
day's punches on the attendance terminal: check_in, pause start/end, check_out and
worked hours (outings computed here, not stored in Odoo). Re-running a sync is idempotent.
The sync is the only writer: HR only reads attendances in Odoo.
"""
import csv
import logging
import os
import sys
import time
import xmlrpc.client
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, time as dtime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

BASE_DIR = Path(__file__).resolve().parent


def load_env(path):
    """Load .env file without overriding existing environment variables."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env(BASE_DIR / ".env")

BIOTIME_URL = os.environ.get("BIOTIME_URL", "http://localhost:8083")
BIOTIME_USER = os.environ.get("BIOTIME_USER", "admin")
BIOTIME_PASS = os.environ.get("BIOTIME_PASS", "admin")

ODOO_URL = os.environ.get("ODOO_URL", "https://votre-instance.odoo.com").strip().rstrip("/")
if not ODOO_URL.startswith(("http://", "https://")):
    ODOO_URL = "https://" + ODOO_URL
ODOO_DB = os.environ.get("ODOO_DB", "votre-base")
ODOO_USER = os.environ.get("ODOO_USER", "admin@societe.com")
ODOO_API_KEY = os.environ.get("ODOO_API_KEY", "votre_cle_api_odoo")
# Company whose employees are synced (multi-company databases); empty = all companies of the user
ODOO_COMPANY = os.environ.get("ODOO_COMPANY", "").strip()

LOCAL_TZ = ZoneInfo(os.environ.get("BIOTIME_TZ", "Europe/Paris"))
DUPLICATE_MINUTES = float(os.environ.get("DUPLICATE_MINUTES", "2"))
# The pause is the longest outing starting within this window; other outings are "sorties"
PAUSE_WINDOW = os.environ.get("PAUSE_WINDOW", "11:30-15:00")
# Outings up to this duration are not deducted (quick errand)
OUTING_TOLERANCE_MINUTES = float(os.environ.get("OUTING_TOLERANCE_MINUTES", "10"))
# Departure used when the last departure of the day was not punched
DEFAULT_CHECKOUT_TIME = os.environ.get("DEFAULT_CHECKOUT_TIME", "18:00")

# Access-only terminals (door opening): their punches are not attendance punches
TERMINALS_IGNORE = {sn.strip() for sn in os.environ.get("TERMINALS_IGNORE", "").split(",") if sn.strip()}
# TERMINALS_IGNORE applies from this date (YYYY-MM-DD); earlier punches all count
TERMINAL_RULES_SINCE = os.environ.get("TERMINAL_RULES_SINCE", "").strip()
# Go-live date (YYYY-MM-DD): the incremental sync ignores punches before it
SYNC_START_DATE = os.environ.get("SYNC_START_DATE", "").strip()
# Terminal clock correction: minutes added to punches whose terminal time is in
# [CLOCK_OFFSET_FROM, CLOCK_OFFSET_UNTIL) ("YYYY-MM-DD HH:MM", empty = no bound)
CLOCK_OFFSET_MINUTES = float(os.environ.get("CLOCK_OFFSET_MINUTES", "0"))
CLOCK_OFFSET_FROM = os.environ.get("CLOCK_OFFSET_FROM", "").strip()
CLOCK_OFFSET_UNTIL = os.environ.get("CLOCK_OFFSET_UNTIL", "").strip()
# Manual corrections (arrival / departure overrides), see corrections.example.csv
CORRECTIONS_FILE = BASE_DIR / os.environ.get("CORRECTIONS_FILE", "corrections.csv")
PAGE_SIZE = 500

# Odoo Studio fields on hr.attendance. Missing or computed fields are not written.
ATTENDANCE_FIELDS = {
    "pause_start": "x_studio_debut_pause",
    "pause_end": "x_studio_fin_pause",
    "hours": "x_studio_heures_travailles",
}
# On hr.employee: outings count as work time (managers, client visits)
PRO_OUTINGS_FIELD = "x_studio_sorties_professionnelles"

FMT = "%Y-%m-%d %H:%M:%S"
log = logging.getLogger("zk_odoo")


def _parse_window(value):
    start, end = (datetime.strptime(v.strip(), "%H:%M").time() for v in value.split("-"))
    return start, end


PAUSE_START, PAUSE_END = _parse_window(PAUSE_WINDOW)
DEFAULT_CHECKOUT = datetime.strptime(DEFAULT_CHECKOUT_TIME, "%H:%M").time()


def setup_logging(name):
    (BASE_DIR / "logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        handlers=[
            logging.FileHandler(BASE_DIR / "logs" / f"{name}.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


@contextmanager
def single_instance(max_age_hours=6):
    """Prevent concurrent script executions using a lock file."""
    lock = BASE_DIR / "zk_odoo_sync.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        if time.time() - lock.stat().st_mtime < max_age_hours * 3600:
            log.warning("Une autre synchronisation est en cours (%s). Abandon.", lock)
            sys.exit(0)
        log.warning("Verrou périmé supprimé : %s", lock)
        lock.unlink()
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def now_local():
    """Current naive datetime in BioTime local timezone."""
    return datetime.now(LOCAL_TZ).replace(tzinfo=None, microsecond=0)


def local_dt_to_utc(value):
    """Convert a naive BioTime local datetime to naive UTC (Odoo storage)."""
    return value.replace(tzinfo=LOCAL_TZ).astimezone(timezone.utc).replace(tzinfo=None)


def local_to_utc(value):
    """Convert BioTime local time string to naive UTC datetime."""
    return local_dt_to_utc(datetime.strptime(value, FMT))


def utc_to_local(value):
    return value.replace(tzinfo=timezone.utc).astimezone(LOCAL_TZ).replace(tzinfo=None)


def correct_clock(punch):
    """Apply the terminal clock correction to a terminal-time punch."""
    raw = f"{punch:%Y-%m-%d %H:%M}"
    if CLOCK_OFFSET_MINUTES and (not CLOCK_OFFSET_FROM or raw >= CLOCK_OFFSET_FROM)             and (not CLOCK_OFFSET_UNTIL or raw < CLOCK_OFFSET_UNTIL):
        return punch + timedelta(minutes=CLOCK_OFFSET_MINUTES)
    return punch


def load_corrections(path=None):
    """Read manual corrections: {(code, date): {"arrival": datetime, "departure": datetime}}.

    CSV (';' separated, Excel-friendly): numero;date;arrivee;depart;commentaire
    """
    path = path or CORRECTIONS_FILE
    corrections = {}
    if not path.exists():
        return corrections
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh, delimiter=";"), start=2):
            try:
                code, day = row["numero"].strip(), datetime.strptime(row["date"].strip(), "%Y-%m-%d").date()
                entry = {}
                for key, col in (("arrival", "arrivee"), ("departure", "depart")):
                    if (row.get(col) or "").strip():
                        entry[key] = datetime.combine(day, datetime.strptime(row[col].strip(), "%H:%M").time())
            except (KeyError, ValueError, AttributeError) as e:
                log.warning("%s ligne %d ignorée (format attendu numero;date;arrivee;depart) : %s", path.name, i, e)
                continue
            if entry:
                corrections.setdefault((code, day), {}).update(entry)
    return corrections


def apply_correction(punches, correction):
    """Override the arrival (first punch) and/or departure (last punch) of a day."""
    punches = sorted(punches)
    if "arrival" in correction:
        punches = [correction["arrival"]] + punches[1:]
    if "departure" in correction:
        if len(punches) % 2 == 0 and len(punches) > 0:
            punches[-1] = correction["departure"]
        else:
            punches.append(correction["departure"])
    return sorted(punches)


def is_door_punch(txn):
    """True for punches on access-only terminals (door opening), which are not attendance."""
    if TERMINAL_RULES_SINCE and (txn.get("punch_time") or "9999")[:10] < TERMINAL_RULES_SINCE:
        return False
    return str(txn.get("terminal_sn") or "").strip() in TERMINALS_IGNORE


# ---------------------------------------------------------------- Day reconstruction

DOOR_ONLY_MSG = "aucun pointage sur la pointeuse intérieure (porte ouverte à {})"


def _hours(start, end):
    return (end - start).total_seconds() / 3600


def build_day(punches, closed, door_punches=(), pro=False):
    """Summarize one employee's day into the values of a single hr.attendance.

    punches      : local datetimes on the attendance terminal, alternating in / out
    closed       : True once the day is over (a missing departure is set to DEFAULT_CHECKOUT_TIME)
    door_punches : local datetimes on access-only terminals, used only without attendance punches
    pro          : outings count as work time, only the pause is deducted
    """
    duplicate = timedelta(minutes=DUPLICATE_MINUTES)
    kept = []
    for p in sorted(punches):
        if not kept or p - kept[-1] > duplicate:
            kept.append(p)

    if not kept:
        first = min(door_punches)
        return {"check_in": first, "check_out": first if closed else None, "pause_start": None,
                "pause_end": None, "outings": [], "outings_count": 0, "outings_hours": 0.0,
                "hours": 0.0, "detail": "", "anomaly": DOOR_ONLY_MSG.format(f"{first:%H:%M}")}

    # in/out pairs, then the gaps between them (time spent outside)
    segments = [(kept[i], kept[i + 1] if i + 1 < len(kept) else None) for i in range(0, len(kept), 2)]
    gaps = [(segments[i][1], segments[i + 1][0]) for i in range(len(segments) - 1)]
    pause = max((g for g in gaps if PAUSE_START <= g[0].time() < PAUSE_END),
                key=lambda g: g[1] - g[0], default=None)
    outings = [g for g in gaps if g is not pause]
    tolerance = timedelta(minutes=OUTING_TOLERANCE_MINUTES)
    outings_hours = sum(_hours(a, b) for a, b in outings if b - a > tolerance)

    check_out, anomalies = None, []
    if len(kept) % 2 == 0:
        check_out = kept[-1]
    elif closed:
        check_out = max(datetime.combine(kept[-1].date(), DEFAULT_CHECKOUT), kept[-1])
        segments[-1] = (kept[-1], check_out)
        anomalies.append(f"départ non pointé : {check_out:%H:%M} retenu"
                         + (" (un seul pointage)" if len(kept) == 1 else ""))

    hours = 0.0
    if check_out:
        hours = _hours(kept[0], check_out) - (_hours(*pause) if pause else 0.0) - (0.0 if pro else outings_hours)
    detail = " | ".join(f"{a:%H:%M}-{b:%H:%M}" if b else f"{a:%H:%M}-…" for a, b in segments)
    return {
        "check_in": kept[0],
        "check_out": check_out,
        "pause_start": pause[0] if pause else None,
        "pause_end": pause[1] if pause else None,
        "outings": outings,
        "outings_count": len(outings),
        "outings_hours": round(outings_hours, 2),
        "hours": round(max(hours, 0.0), 2),
        "detail": detail,
        "anomaly": "; ".join(anomalies),
    }


def group_punches(txns, first_day, last_day, corrections=None):
    """Group BioTime transactions by employee code and local day, with clock and manual corrections.

    Returns (attendance, door, names): {code: {date: [local datetime]}} for attendance and
    access-only punches, and {code: BioTime name}. Corrections only apply to days in
    [first_day, last_day], the days whose punches were all fetched.
    """
    attendance, door = defaultdict(lambda: defaultdict(list)), defaultdict(lambda: defaultdict(list))
    names, seen = {}, set()
    for txn in txns:
        code = str(txn.get("emp_code") or "").strip()
        if txn.get("id") in seen or not code or not txn.get("punch_time"):
            continue
        seen.add(txn.get("id"))
        names[code] = " ".join(filter(None, [txn.get("first_name"), txn.get("last_name")]))
        local = correct_clock(datetime.strptime(txn["punch_time"], FMT))
        (door if is_door_punch(txn) else attendance)[code][local.date()].append(local)
    for (code, day), correction in (load_corrections() if corrections is None else corrections).items():
        if not first_day <= day <= last_day:
            continue
        attendance[code][day] = apply_correction(attendance[code].get(day, []), correction)
        log.info("Correction manuelle appliquée : n°%s le %s", code, day)
    return attendance, door, names


def build_days(code_attendance, code_door, pro=False, today=None):
    """{date: day summary} for one employee; days before `today` are closed."""
    today = today or now_local().date()
    return {day: build_day(code_attendance.get(day, []), day < today, code_door.get(day, []), pro)
            for day in sorted(set(code_attendance) | set(code_door))}


def attendance_values(day, fields):
    """hr.attendance values (UTC) for a day summary, limited to the writable Studio fields."""
    utc = lambda d: local_dt_to_utc(d).strftime(FMT) if d else False
    vals = {"check_in": utc(day["check_in"]), "check_out": utc(day["check_out"])}
    data = {"pause_start": utc(day["pause_start"]), "pause_end": utc(day["pause_end"]), "hours": day["hours"]}
    for key, value in data.items():
        if key in fields:
            vals[fields[key]] = value
    return vals


def _same(odoo_value, value):
    if isinstance(value, float):
        return round(odoo_value or 0.0, 2) == round(value, 2)
    return (odoo_value or False) == (value or False)


# ---------------------------------------------------------------- BioTime

class BioTime:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        self._login()

    def _login(self):
        res = self.session.post(f"{BIOTIME_URL}/api-token-auth/",
                                json={"username": BIOTIME_USER, "password": BIOTIME_PASS}, timeout=15)
        if res.status_code != 200:
            raise RuntimeError(f"Authentification BioTime refusée : {res.status_code} {res.text}")
        self.session.headers["Authorization"] = f"Token {res.json()['token']}"

    def _get(self, path, params):
        res = self.session.get(f"{BIOTIME_URL}{path}", params=params, timeout=60)
        if res.status_code in (401, 403):
            self._login()
            res = self.session.get(f"{BIOTIME_URL}{path}", params=params, timeout=60)
        res.raise_for_status()
        return res.json()

    def transactions(self, start_time, end_time):
        """Fetch all transactions between start_time and end_time."""
        page = 1
        while True:
            payload = self._get("/iclock/api/transactions/", {
                "start_time": start_time.strftime(FMT),
                "end_time": end_time.strftime(FMT),
                "page": page,
                "page_size": PAGE_SIZE,
            })
            data = payload.get("data", [])
            yield from data
            log.info("BioTime page %d : %d pointages (total annoncé : %s)", page, len(data), payload.get("count"))
            if not payload.get("next") or not data:
                break
            page += 1

    def terminals(self):
        page = 1
        while True:
            payload = self._get("/iclock/api/terminals/", {"page": page, "page_size": PAGE_SIZE})
            yield from payload.get("data", [])
            if not payload.get("next"):
                break
            page += 1


# ---------------------------------------------------------------- Odoo

class Odoo:
    def __init__(self):
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common", allow_none=True)
        self.uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_API_KEY, {})
        if not self.uid:
            raise RuntimeError("Authentification Odoo refusée (vérifiez base, utilisateur et clé API)")
        self.models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object", allow_none=True)
        self.company_id, self.context = None, {}
        if ODOO_COMPANY:
            company = self.call("res.company", "search", [["name", "=", ODOO_COMPANY]], limit=1)
            if not company:
                raise RuntimeError(f"Société Odoo introuvable ou non autorisée pour cet utilisateur : {ODOO_COMPANY}")
            self.company_id, self.context = company[0], {"allowed_company_ids": company}

    def call(self, model, method, *args, **kwargs):
        if self.context:
            kwargs.setdefault("context", self.context)
        return self.models.execute_kw(ODOO_DB, self.uid, ODOO_API_KEY, model, method, list(args), kwargs)

    def employee_map(self):
        """Map BioTime emp_code to Odoo employee via barcode or identification_id."""
        fields = ["name", "barcode", "identification_id"]
        has_pro = PRO_OUTINGS_FIELD in self.call("hr.employee", "fields_get", attributes=["type"])
        domain = [["company_id", "=", self.company_id]] if self.company_id else []
        employees = self.call("hr.employee", "search_read", domain,
                              fields=fields + ([PRO_OUTINGS_FIELD] if has_pro else []))
        mapping = {}
        for emp in employees:
            emp["pro"] = bool(emp.get(PRO_OUTINGS_FIELD))
            # Barcode takes precedence over identification_id
            for key in (emp["identification_id"], emp["barcode"]):
                if key:
                    mapping[str(key).strip()] = emp
        return mapping

    def writable_attendance_fields(self):
        """Studio fields that exist on hr.attendance and are not computed by Odoo: {key: name}."""
        defs = {f["name"]: f for f in self.call("ir.model.fields", "search_read",
                                                [["model", "=", "hr.attendance"],
                                                 ["name", "in", list(ATTENDANCE_FIELDS.values())]],
                                                fields=["name", "compute"])}
        fields = {}
        for key, name in ATTENDANCE_FIELDS.items():
            if name not in defs:
                log.warning("Champ %s absent de hr.attendance : non synchronisé", name)
            elif defs[name]["compute"]:
                log.info("Champ %s calculé par Odoo : non écrit par le script", name)
            else:
                fields[key] = name
        return fields


def sync_employee(odoo, emp, days, fields):
    """Create or update one hr.attendance per day for an employee. Returns (created, updated)."""
    first, last = min(days), max(days)
    start = local_dt_to_utc(datetime.combine(first, dtime.min)).strftime(FMT)
    end = local_dt_to_utc(datetime.combine(last + timedelta(days=1), dtime.min)).strftime(FMT)
    read = ["check_in", "check_out"] + list(fields.values())
    existing = defaultdict(list)
    for att in odoo.call("hr.attendance", "search_read",
                         [["employee_id", "=", emp["id"]], ["check_in", ">=", start], ["check_in", "<", end]],
                         fields=read):
        existing[utc_to_local(datetime.strptime(att["check_in"], FMT)).date()].append(att)

    created = updated = 0
    # Chronological order: Odoo refuses a new attendance while the previous one is still open
    for day in sorted(days):
        summary, records = days[day], existing.get(day, [])
        if summary["anomaly"]:
            log.warning("%s %s : %s", emp["name"], day, summary["anomaly"])
        if len(records) > 1:
            log.warning("%s %s : %d présences dans Odoo pour ce jour, non modifiées (à fusionner à la main)",
                        emp["name"], day, len(records))
            continue
        vals = attendance_values(summary, fields)
        if not records:
            odoo.call("hr.attendance", "create", [{"employee_id": emp["id"], **vals}])
            created += 1
            continue
        record = records[0]
        changes = {k: v for k, v in vals.items() if not _same(record.get(k), v)}
        if changes:
            odoo.call("hr.attendance", "write", [record["id"]], changes)
            updated += 1
    return created, updated


def run(start_time, end_time):
    """Sync BioTime punches of the days in [start_time, end_time] to Odoo. Returns error count."""
    start_time = datetime.combine(start_time.date(), dtime.min)  # always rebuild whole days
    log.info("Synchronisation des pointages du %s au %s", start_time, end_time)
    biotime = BioTime()
    odoo = Odoo()
    employees = odoo.employee_map()
    fields = odoo.writable_attendance_fields()

    attendance, door, names = group_punches(biotime.transactions(start_time, end_time),
                                            start_time.date(), end_time.date())
    codes = sorted(set(attendance) | set(door), key=lambda c: (len(c), c))
    log.info("%d employé(s) avec des pointages", len(codes))

    unknown = [f"{c} ({names.get(c, '')})" for c in codes if c not in employees]
    if unknown:
        log.warning("Codes BioTime introuvables dans Odoo (Badge ID / Matricule) : %s", ", ".join(unknown))

    errors = created = updated = 0
    for code in codes:
        emp = employees.get(code)
        if not emp:
            continue
        days = build_days(attendance.get(code, {}), door.get(code, {}), emp["pro"])
        try:
            c, u = sync_employee(odoo, emp, days, fields)
            created, updated = created + c, updated + u
        except (xmlrpc.client.Fault, OSError) as e:
            errors += 1
            log.error("%s (code %s) : échec de l'envoi vers Odoo : %s", emp["name"], code, e)

    log.info("Terminé : %d présence(s) créée(s), %d mise(s) à jour, %d erreur(s)", created, updated, errors)
    return errors
