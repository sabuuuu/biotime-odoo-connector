"""Generate an Excel preview of ZKBioTime attendance data."""
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

import zk_odoo_sync as zk

RAW_COLUMNS = [
    ("id", "ID BioTime"),
    ("emp_code", "Numéro d'employé"),
    ("first_name", "Prénom"),
    ("last_name", "Nom"),
    ("department", "Département"),
    ("punch_time", "Temps de pointage"),
    ("punch_state", "Etat (code)"),
    ("punch_state_display", "Etat du pointage"),
    ("verify_type_display", "Vérifier type"),
    ("work_code", "Code de travail"),
    ("terminal_sn", "N° série pointeuse"),
    ("terminal_alias", "Pointeuse"),
    ("area_alias", "Zone"),
    ("upload_time", "Heure de remontée"),
]
WARN_FILL = PatternFill("solid", fgColor="FFF2CC")
DAYS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

WORK_DAYS = {int(d) for d in os.environ.get("WORK_DAYS", "0,1,2,3").split(",")}
DAILY_HOURS = float(os.environ.get("DAILY_HOURS", "9"))
BREAK_HOURS = float(os.environ.get("BREAK_MINUTES", "60")) / 60
SHORT_DAY_HOURS = float(os.environ.get("SHORT_DAY_HOURS", "6"))


def add_sheet(wb, title, headers, rows, warn_col=None):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in rows:
        ws.append(row)
        if warn_col is not None and row[warn_col]:
            for cell in ws[ws.max_row]:
                cell.fill = WARN_FILL
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for i, header in enumerate(headers, 1):
        width = max([len(str(header))] + [len(str(r[i - 1])) for r in rows[:500]])
        ws.column_dimensions[get_column_letter(i)].width = min(width + 2, 60)


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d")


def main():
    end = parse_date(sys.argv[2]) + timedelta(days=1, seconds=-1) if len(sys.argv) > 2 else zk.now_local()
    start = parse_date(sys.argv[1]) if len(sys.argv) > 1 else (end - timedelta(days=30)).replace(hour=0, minute=0, second=0)

    print(f"Lecture des pointages BioTime du {start} au {end}...")
    biotime = zk.BioTime()
    txns = {t["id"]: t for t in biotime.transactions(start, end)}
    txns = sorted(txns.values(), key=lambda t: (str(t.get("emp_code")), t.get("punch_time") or ""))
    print(f"{len(txns)} pointages récupérés.")

    names, punches, door_days = {}, defaultdict(list), defaultdict(set)
    for t in txns:
        code = str(t.get("emp_code") or "").strip()
        if code and t.get("punch_time"):
            names[code] = " ".join(filter(None, [t.get("first_name"), t.get("last_name")]))
            if zk.punch_direction(t) == "ignore":
                door_days[code].add(datetime.strptime(t["punch_time"], zk.FMT).date())
            else:
                punches[code].append((zk.local_to_utc(t["punch_time"]), zk.punch_direction(t)))

    per_terminal = Counter(str(t.get("terminal_sn") or "") for t in txns)
    try:
        terminals = {str(d.get("sn")): d for d in biotime.terminals()}
    except Exception as e:
        print(f"Liste des pointeuses indisponible : {e}")
        terminals = {}
    sens = {"in": "Entrée", "out": "Sortie", None: "Alternance entrée/sortie", "ignore": "Ignoré (ouverture porte)"}
    terminal_rows = [[sn, d.get("alias") or "", d.get("area_name") or "", d.get("ip_address") or "",
                      d.get("last_activity") or "", sens[zk.punch_direction({"terminal_sn": sn})], per_terminal.get(sn, 0)]
                     for sn, d in terminals.items()]
    terminal_rows += [[sn, "", "", "", "", sens[zk.punch_direction({"terminal_sn": sn})], n]
                      for sn, n in per_terminal.items() if sn not in terminals]

    planned, daily, anomalies, summary = [], [], [], []
    fmt = lambda d: zk.utc_to_local(d).strftime(zk.FMT) if d else ""
    for code in sorted(punches, key=lambda c: (len(c), c)):
        _, records, notes = zk.plan_attendances(None, sorted(punches[code], key=lambda p: p[0]))
        incomplete, by_day = 0, defaultdict(list)
        for check_in, check_out, remark in records:
            day = zk.utc_to_local(check_in).date()
            hours = round((check_out - check_in).total_seconds() / 3600, 2) if check_out else ""
            if remark or not check_out:
                incomplete += 1
            remark = remark or ("en cours (pas encore de sortie)" if not check_out else "")
            by_day[day].append((check_in, check_out, remark))
            planned.append([code, names[code], day.isoformat(), DAYS_FR[day.weekday()],
                            fmt(check_in), fmt(check_out), hours, remark])

        total_net, total_extra = 0.0, 0.0
        for day, atts in sorted(by_day.items()):
            done = [(i, o) for i, o, _ in atts if o and o > i]
            presence = sum((o - i).total_seconds() for i, o in done) / 3600
            # Deduct break if not already clocked
            gaps = sum((done[k + 1][0] - done[k][1]).total_seconds() for k in range(len(done) - 1)) / 3600
            deducted = max(0.0, BREAK_HOURS - gaps) if presence > SHORT_DAY_HOURS else 0.0
            net = max(0.0, presence - deducted)
            expected = DAILY_HOURS if day.weekday() in WORK_DAYS else 0.0
            remarks = [r for _, _, r in atts if r]
            if day.weekday() not in WORK_DAYS:
                remarks.append("hors jours ouvrés (heures sup ?)")
            elif not remarks and presence < SHORT_DAY_HOURS:
                remarks.append(f"journée courte (< {SHORT_DAY_HOURS:g} h) : sortie manquante ?")
            extra = net - expected if not remarks or day.weekday() not in WORK_DAYS else 0.0
            total_net += net
            total_extra += max(extra, 0)
            daily.append([code, names[code], day.isoformat(), DAYS_FR[day.weekday()],
                          fmt(atts[0][0]), fmt(atts[-1][1]), round(presence, 2), round(gaps, 2),
                          round(deducted, 2), round(net, 2), expected, round(extra, 2), "; ".join(remarks)])
        for t, msg in notes:
            anomalies.append([code, names[code], fmt(t), msg])
        days = {zk.utc_to_local(p).date() for p, _ in punches[code]}
        summary.append([code, names[code], len(punches[code]), len(days), len(records), incomplete,
                        round(total_net, 2), round(total_extra, 2)])

    for code, days in zk.door_only_days(door_days, punches).items():
        for day in days:
            anomalies.append([code, names[code], day.isoformat(), zk.DOOR_ONLY_MSG])

    wb = Workbook()
    wb.remove(wb.active)
    add_sheet(wb, "Pointeuses", ["N° série", "Nom", "Zone", "Adresse IP", "Dernière activité",
                                 "Sens (.env)", "Nb pointages sur la période"], terminal_rows)
    add_sheet(wb, "Pointages bruts", [h for _, h in RAW_COLUMNS] + ["Sens (déduit)"],
              [[t.get(k) if t.get(k) is not None else "" for k, _ in RAW_COLUMNS]
               + [sens[zk.punch_direction(t)]] for t in txns])
    add_sheet(wb, "Présences prévues Odoo",
              ["Numéro d'employé", "Nom", "Date", "Jour", "Entrée", "Sortie", "Durée (h)", "Remarque"],
              planned, warn_col=7)
    add_sheet(wb, "Heures par jour",
              ["Numéro d'employé", "Nom", "Date", "Jour", "Première entrée", "Dernière sortie", "Présence (h)",
               "Pause pointée (h)", "Pause déduite (h)", "Heures nettes", "Heures prévues",
               "Écart / heures sup", "Remarque"], daily, warn_col=12)
    add_sheet(wb, "Anomalies", ["Numéro d'employé", "Nom", "Pointage", "Détail"], anomalies)
    add_sheet(wb, "Résumé par employé",
              ["Numéro d'employé", "Nom", "Nb pointages", "Nb jours pointés", "Nb présences",
               "Présences incomplètes", "Heures nettes", "Heures sup (jours complets)"], summary, warn_col=5)

    out = zk.BASE_DIR / f"apercu_biotime_{start:%Y%m%d}_{end:%Y%m%d}.xlsx"
    wb.save(out)
    print(f"Fichier généré : {out}")
    print(f"  {len(planned)} présences prévues, {len(anomalies)} anomalie(s), {len(summary)} employé(s)")


if __name__ == "__main__":
    main()
