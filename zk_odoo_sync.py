"""ZKBioTime to Odoo (hr.attendance) synchronization logic."""
import logging
import os
import sys
import time
import xmlrpc.client
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
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

LOCAL_TZ = ZoneInfo(os.environ.get("BIOTIME_TZ", "Europe/Paris"))
MAX_SHIFT_HOURS = float(os.environ.get("MAX_SHIFT_HOURS", "16"))
SAME_DAY_ONLY = os.environ.get("SAME_DAY_ONLY", "1") == "1"
DUPLICATE_MINUTES = float(os.environ.get("DUPLICATE_MINUTES", "2"))

TERMINALS_IN = {sn.strip() for sn in os.environ.get("TERMINALS_IN", "").split(",") if sn.strip()}
TERMINALS_OUT = {sn.strip() for sn in os.environ.get("TERMINALS_OUT", "").split(",") if sn.strip()}
PAGE_SIZE = 500

FMT = "%Y-%m-%d %H:%M:%S"
log = logging.getLogger("zk_odoo")


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


def local_to_utc(value):
    """Convert BioTime local time string to naive UTC datetime."""
    local = datetime.strptime(value, FMT).replace(tzinfo=LOCAL_TZ)
    return local.astimezone(timezone.utc).replace(tzinfo=None)


def utc_to_local(value):
    return value.replace(tzinfo=timezone.utc).astimezone(LOCAL_TZ).replace(tzinfo=None)


def punch_direction(txn):
    """Determine punch direction ('in', 'out', or None) from terminal serial."""
    sn = str(txn.get("terminal_sn") or "").strip()
    if sn in TERMINALS_IN:
        return "in"
    if sn in TERMINALS_OUT:
        return "out"
    return None


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


class Odoo:
    def __init__(self):
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common", allow_none=True)
        self.uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_API_KEY, {})
        if not self.uid:
            raise RuntimeError("Authentification Odoo refusée (vérifiez base, utilisateur et clé API)")
        self.models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object", allow_none=True)

    def call(self, model, method, *args, **kwargs):
        return self.models.execute_kw(ODOO_DB, self.uid, ODOO_API_KEY, model, method, list(args), kwargs)

    def employee_map(self):
        """Map BioTime emp_code to Odoo employee via barcode or identification_id."""
        employees = self.call("hr.employee", "search_read", [],
                              fields=["name", "barcode", "identification_id"])
        mapping = {}
        for emp in employees:
            # Barcode takes precedence over identification_id
            for key in (emp["identification_id"], emp["barcode"]):
                if key:
                    mapping[str(key).strip()] = emp
        return mapping

    def last_attendance(self, employee_id):
        res = self.call("hr.attendance", "search_read", [["employee_id", "=", employee_id]],
                        fields=["check_in", "check_out"], order="check_in desc", limit=1)
        if not res:
            return None
        att = res[0]
        return {
            "id": att["id"],
            "check_in": datetime.strptime(att["check_in"], FMT),
            "check_out": datetime.strptime(att["check_out"], FMT) if att["check_out"] else None,
        }

    def attendance_times(self, employee_id, since):
        """Get existing check-in/out timestamps in Odoo since given time."""
        res = self.call("hr.attendance", "search_read",
                        [["employee_id", "=", employee_id], ["check_in", ">=", since.strftime(FMT)]],
                        fields=["check_in", "check_out"])
        return [datetime.strptime(v, FMT) for att in res for v in (att["check_in"], att["check_out"]) if v]


def plan_attendances(last, punches, known=()):
    """Convert sorted UTC punches into Odoo attendance records."""
    max_shift = timedelta(hours=MAX_SHIFT_HOURS)
    duplicate = timedelta(minutes=DUPLICATE_MINUTES)
    close_last_at, records, notes = None, [], []

    open_in = last["check_in"] if last and not last["check_out"] else None
    open_is_last = open_in is not None
    last_event = (last["check_out"] or last["check_in"]) if last else None

    def close_open(at, remark=""):
        nonlocal open_in, open_is_last, close_last_at, last_event
        if open_is_last:
            close_last_at = at
            open_is_last = False
        else:
            records[-1][1] = at
            if remark:
                records[-1][2] = remark
        if remark:
            notes.append((open_in, f"{remark}, à corriger dans Odoo"))
        open_in = None
        last_event = max(last_event, at)

    for t, direction in punches:
        if last_event and t <= last_event + duplicate:
            if not any(abs(t - k) <= duplicate for k in known):
                if t < last_event:
                    notes.append((t, "antérieur au dernier pointage Odoo, ignoré (à saisir manuellement si besoin)"))
                elif t > last_event:
                    notes.append((t, f"doublon (< {DUPLICATE_MINUTES:g} min après le précédent), ignoré"))
            continue

        if open_in is not None and (t - open_in > max_shift or (
                SAME_DAY_ONLY and utc_to_local(t).date() != utc_to_local(open_in).date())):
            close_open(open_in, "sortie oubliée : clôturée à 0 h")

        if direction is None:
            direction = "out" if open_in is not None else "in"

        if direction == "out":
            if open_in is not None:
                close_open(t)
            else:
                records.append([t, t, "entrée manquante : présence à 0 h"])
                notes.append((t, "sortie sans entrée : présence à 0 h, à corriger dans Odoo"))
                last_event = t
            continue

        if open_in is not None:
            close_open(open_in, "deux entrées de suite (sortie manquante) : clôturée à 0 h")
        records.append([t, None, ""])
        open_in = t
        last_event = t

    return close_last_at, records, notes


def push_employee(odoo, emp, punches):
    last = odoo.last_attendance(emp["id"])
    known = odoo.attendance_times(emp["id"], punches[0][0] - timedelta(hours=MAX_SHIFT_HOURS)) if last else []
    close_last_at, records, notes = plan_attendances(last, punches, known)

    for t, msg in notes:
        log.warning("%s (%s UTC) : %s", emp["name"], t, msg)
    if close_last_at:
        odoo.call("hr.attendance", "write", [last["id"]], {"check_out": close_last_at.strftime(FMT)})
    if records:
        vals = []
        for check_in, check_out, _ in records:
            v = {"employee_id": emp["id"], "check_in": check_in.strftime(FMT)}
            if check_out:
                v["check_out"] = check_out.strftime(FMT)
            vals.append(v)
        odoo.call("hr.attendance", "create", vals)
    if close_last_at or records:
        log.info("%s : %d présence(s) créée(s)%s", emp["name"], len(records),
                 ", 1 sortie enregistrée" if close_last_at else "")


def run(start_time, end_time):
    """Sync BioTime punches within [start_time, end_time] to Odoo. Returns error count."""
    log.info("Synchronisation des pointages du %s au %s", start_time, end_time)
    biotime = BioTime()
    odoo = Odoo()
    employees = odoo.employee_map()

    seen, punches_by_code, unknown_terminals = set(), defaultdict(list), set()
    for txn in biotime.transactions(start_time, end_time):
        code = str(txn.get("emp_code") or "").strip()
        if txn["id"] in seen or not code or not txn.get("punch_time"):
            continue
        seen.add(txn["id"])
        punches_by_code[code].append((local_to_utc(txn["punch_time"]), punch_direction(txn)))
        if (TERMINALS_IN or TERMINALS_OUT) and punch_direction(txn) is None:
            unknown_terminals.add(str(txn.get("terminal_sn")))
    log.info("%d pointages récupérés pour %d employé(s)", len(seen), len(punches_by_code))
    if unknown_terminals:
        log.warning("Pointeuse(s) ni en entrée ni en sortie dans .env (alternance utilisée) : %s",
                    ", ".join(sorted(unknown_terminals)))

    unknown = sorted(c for c in punches_by_code if c not in employees)
    if unknown:
        log.warning("Codes BioTime introuvables dans Odoo (Badge ID / Matricule) : %s", ", ".join(unknown))

    errors = 0
    for code, punches in punches_by_code.items():
        emp = employees.get(code)
        if not emp:
            continue
        try:
            push_employee(odoo, emp, sorted(punches, key=lambda p: p[0]))
        except (xmlrpc.client.Fault, OSError) as e:
            errors += 1
            log.error("%s (code %s) : échec de l'envoi vers Odoo : %s", emp["name"], code, e)

    log.info("Terminé : %d erreur(s)", errors)
    return errors
