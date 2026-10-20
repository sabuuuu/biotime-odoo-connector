"""Tests for day reconstruction and Odoo upsert. Run: python -m unittest -v"""
import os
import unittest
from datetime import date, datetime

# Fixed settings so the tests do not depend on the local .env
os.environ.update({"BIOTIME_TZ": "Africa/Algiers", "DUPLICATE_MINUTES": "2", "PAUSE_WINDOW": "11:30-15:00",
                   "OUTING_TOLERANCE_MINUTES": "10", "DEFAULT_CHECKOUT_TIME": "18:00",
                   "TERMINALS_IGNORE": "DOOR", "TERMINAL_RULES_SINCE": "", "WORK_DAYS": "0,1,2,3",
                   "CLOCK_OFFSETS": "2026-10-05 00:00|2026-10-05 07:00|120; 2026-10-05 07:00|2026-10-05 07:30|60"})
import zk_odoo_sync as zk  # noqa: E402

DAY = date(2026, 10, 5)


def at(*times):
    return [datetime.combine(DAY, datetime.strptime(t, "%H:%M").time()) for t in times]


class BuildDayTest(unittest.TestCase):
    def test_standard_day_four_punches(self):
        d = zk.build_day(at("08:01", "12:30", "13:25", "18:05"), closed=True)
        self.assertEqual((d["check_in"], d["pause_start"], d["pause_end"], d["check_out"]),
                         tuple(at("08:01", "12:30", "13:25", "18:05")))
        self.assertEqual(d["hours"], 9.15)  # 10h04 - 55 min
        self.assertEqual((d["outings_count"], d["anomaly"]), (0, ""))

    def test_no_pause_punched_deducts_nothing(self):
        d = zk.build_day(at("08:00", "18:00"), closed=True)
        self.assertEqual((d["pause_start"], d["hours"]), (None, 10.0))

    def test_short_outing_tolerated_long_outing_deducted(self):
        d = zk.build_day(at("08:00", "10:00", "10:08", "12:30", "13:30", "15:00", "15:40", "18:00"), closed=True)
        self.assertEqual((d["pause_start"], d["pause_end"]), tuple(at("12:30", "13:30")))
        self.assertEqual((d["outings_count"], d["outings_hours"]), (2, 0.67))  # 8 min free, 40 min deducted
        self.assertEqual(d["hours"], 10 - 1 - 0.67)

    def test_pro_outings_count_as_work(self):
        d = zk.build_day(at("08:00", "10:00", "11:00", "12:30", "13:30", "18:00"), closed=True, pro=True)
        self.assertEqual((d["outings_hours"], d["hours"]), (1.0, 9.0))  # only the pause is deducted

    def test_pause_is_longest_gap_in_window(self):
        d = zk.build_day(at("08:00", "11:40", "11:50", "12:30", "13:30", "18:00"), closed=True)
        self.assertEqual((d["pause_start"], d["pause_end"]), tuple(at("12:30", "13:30")))
        self.assertEqual(d["outings_count"], 1)  # 10 min at 11:40, tolerated

    def test_gap_outside_window_is_not_the_pause(self):
        d = zk.build_day(at("08:00", "16:00", "16:30", "18:00"), closed=True)
        self.assertEqual((d["pause_start"], d["outings_count"], d["outings_hours"]), (None, 1, 0.5))

    def test_duplicates_ignored(self):
        d = zk.build_day(at("08:00", "08:01", "18:00"), closed=True)
        self.assertEqual((d["check_out"], d["anomaly"]), (at("18:00")[0], ""))

    def test_day_in_progress(self):
        d = zk.build_day(at("08:00", "12:30", "13:30"), closed=False)
        self.assertEqual((d["check_out"], d["hours"], d["anomaly"]), (None, 0.0, ""))
        self.assertEqual(d["detail"], "08:00-12:30 | 13:30-…")

    def test_lunch_in_progress_is_not_departure(self):
        d = zk.build_day(at("07:38", "13:03"), closed=False)
        self.assertEqual((d["check_out"], d["pause_start"], d["pause_end"], d["hours"]), (None, at("13:03")[0], None, 0.0))
        self.assertEqual(d["detail"], "07:38-13:03 | pause en cours")

    def test_left_at_lunch_and_never_came_back(self):
        d = zk.build_day(at("07:38", "13:03"), closed=True)
        self.assertEqual((d["check_out"], d["pause_start"], d["hours"]), (at("13:03")[0], None, 5.42))

    def test_departure_after_pause_window_while_day_open(self):
        d = zk.build_day(at("08:00", "12:30", "13:30", "18:00"), closed=False)
        self.assertEqual((d["check_out"], d["hours"]), (at("18:00")[0], 9.0))

    def test_door_arrival_when_no_inside_punch_in_the_morning(self):
        d = zk.build_day(at("13:07", "13:48"), closed=False, door_punches=at("08:04"))
        self.assertEqual((d["check_in"], d["pause_start"], d["pause_end"], d["check_out"]),
                         (*at("08:04", "13:07", "13:48"), None))
        self.assertIn("porte 08:04 retenue", d["anomaly"])

    def test_door_arrival_not_used_when_inside_punched_in_the_morning(self):
        # inside arrival punched late (08:40) or departure forgotten: no door arrival
        d = zk.build_day(at("08:40", "12:30", "13:30"), closed=True, door_punches=at("08:05"))
        self.assertEqual(d["check_in"], at("08:40")[0])
        self.assertNotIn("porte", d["anomaly"])

    def test_door_arrival_skipped_when_arrival_corrected(self):
        d = zk.build_day(at("13:07", "13:48"), closed=False, door_punches=at("08:04"), door_arrival=False)
        self.assertEqual(d["check_in"], at("13:07")[0])

    def test_door_only_non_working_day_skipped(self):
        friday = date(2026, 10, 16)
        door = {friday: [datetime(2026, 10, 16, 15, 9)]}
        self.assertEqual(zk.build_days({}, door, today=date(2026, 10, 20)), {})
        # real punches on a non-working day are kept (overtime)
        attendance = {friday: [datetime(2026, 10, 16, 15, 0), datetime(2026, 10, 16, 17, 0)]}
        self.assertEqual(zk.build_days(attendance, door, today=date(2026, 10, 20))[friday]["hours"], 2.0)

    def test_missing_departure_set_to_18h(self):
        d = zk.build_day(at("08:00", "12:30", "13:30"), closed=True)
        self.assertEqual((d["check_out"], d["hours"]), (at("18:00")[0], 9.0))
        self.assertEqual(d["detail"], "08:00-12:30 | 13:30-18:00")
        self.assertIn("départ non pointé", d["anomaly"])

    def test_single_punch_set_to_18h(self):
        d = zk.build_day(at("08:00"), closed=True)
        self.assertEqual((d["check_out"], d["hours"]), (at("18:00")[0], 10.0))
        self.assertIn("un seul pointage", d["anomaly"])

    def test_missing_departure_after_18h_keeps_last_punch(self):
        d = zk.build_day(at("08:00", "12:30", "13:30", "18:10", "18:40"), closed=True)
        self.assertEqual((d["check_out"], d["outings_hours"]), (at("18:40")[0], 0.5))

    def test_door_only_day(self):
        d = zk.build_day([], closed=True, door_punches=at("08:02", "13:40"))
        self.assertEqual((d["check_in"], d["check_out"], d["hours"]), (at("08:02")[0], at("08:02")[0], 0.0))
        self.assertIn("aucun pointage sur la pointeuse intérieure", d["anomaly"])

    def test_door_punches_ignored_when_inside_punches_exist(self):
        txns = [{"id": 1, "emp_code": "21", "punch_time": "2026-10-05 07:59:00", "terminal_sn": "DOOR"},
                {"id": 2, "emp_code": "21", "punch_time": "2026-10-05 08:00:00", "terminal_sn": "INSIDE"},
                {"id": 2, "emp_code": "21", "punch_time": "2026-10-05 08:00:00", "terminal_sn": "INSIDE"},
                {"id": 3, "emp_code": "21", "punch_time": "2026-10-05 18:00:00", "terminal_sn": "INSIDE"}]
        attendance, door, _, _ = zk.group_punches(txns, DAY, DAY, corrections={})
        days = zk.build_days(attendance["21"], door["21"], today=date(2026, 10, 6))
        self.assertEqual((days[DAY]["check_in"], days[DAY]["hours"]), (at("08:00")[0], 10.0))

    def test_values_converted_to_utc(self):
        vals = zk.attendance_values(zk.build_day(at("08:00", "18:00"), closed=True), {"hours": "x_h"})
        self.assertEqual(vals, {"check_in": "2026-10-05 07:00:00", "check_out": "2026-10-05 17:00:00", "x_h": 10.0})


class CorrectionTest(unittest.TestCase):
    def test_clock_offset_window(self):
        self.assertEqual(zk.correct_clock(at("05:38")[0]), at("07:38")[0])  # first window, +2 h
        self.assertEqual(zk.correct_clock(at("07:07")[0]), at("08:07")[0])  # second window, +1 h
        self.assertEqual(zk.correct_clock(at("10:31")[0]), at("10:31")[0])  # terminals fixed
        self.assertEqual(zk.correct_clock(datetime(2026, 10, 4, 7, 0)), datetime(2026, 10, 4, 7, 0))

    def test_arrival_override_replaces_first_punch(self):
        self.assertEqual(zk.apply_correction(at("08:07", "12:30"), {"arrival": at("08:00")[0]}), at("08:00", "12:30"))
        self.assertEqual(zk.apply_correction([], {"arrival": at("07:55")[0]}), at("07:55"))

    def test_arrival_replaces_late_first_punch(self):
        # first inside punch 20 min 26 s after the corrected arrival: still the arrival
        punch = datetime.combine(DAY, datetime.strptime("08:15:26", "%H:%M:%S").time())
        self.assertEqual(zk.apply_correction([punch] + at("13:31", "14:11", "18:03"), {"arrival": at("07:55")[0]}),
                         at("07:55", "13:31", "14:11", "18:03"))

    def test_arrival_added_when_inside_arrival_missing(self):
        # only the door was punched in the morning: the lunch punches must be kept
        self.assertEqual(zk.apply_correction(at("13:07", "13:48"), {"arrival": at("08:04")[0]}),
                         at("08:04", "13:07", "13:48"))

    def test_departure_override(self):
        self.assertEqual(zk.apply_correction(at("08:00", "17:40"), {"departure": at("18:00")[0]}), at("08:00", "18:00"))
        self.assertEqual(zk.apply_correction(at("08:00"), {"departure": at("18:00")[0]}), at("08:00", "18:00"))

    def test_pause_correction_outside_window(self):
        punches = zk.apply_correction(at("08:26", "11:15", "12:50", "18:45"),
                                      {"pause_start": at("11:15")[0], "pause_end": at("12:46")[0]})
        self.assertEqual(punches, at("08:26", "11:15", "12:46", "18:45"))
        d = zk.build_day(punches, closed=True, forced_pause=tuple(at("11:15", "12:46")))
        self.assertEqual((d["pause_start"], d["pause_end"], d["outings_count"]), (*at("11:15", "12:46"), 0))
        self.assertEqual(d["hours"], 8.8)  # 10h19 - 1h31 = 8h48

    def test_pause_correction_adds_missing_return(self):
        punches = zk.apply_correction(at("08:15", "13:48", "18:07"),
                                      {"pause_start": at("13:48")[0], "pause_end": at("14:40")[0]})
        self.assertEqual(punches, at("08:15", "13:48", "14:40", "18:07"))

    def test_pause_correction_only_replaces_closest_punch(self):
        punches = zk.apply_correction(at("07:22", "12:56", "13:36", "13:59", "18:09"),
                                      {"pause_start": at("13:56")[0], "pause_end": at("14:50")[0]})
        self.assertEqual(punches, at("07:22", "12:56", "13:36", "13:56", "14:50", "18:09"))

    def test_ignored_test_punches(self):
        txns = [{"id": 1, "emp_code": "1", "punch_time": "2026-10-05 09:31:18", "terminal_sn": "DOOR"},
                {"id": 2, "emp_code": "1", "punch_time": "2026-10-05 11:13:28", "terminal_sn": "INSIDE"},
                {"id": 3, "emp_code": "1", "punch_time": "2026-10-05 11:13:50", "terminal_sn": "DOOR"},
                {"id": 4, "emp_code": "15", "punch_time": "2026-10-05 11:13:05", "terminal_sn": "INSIDE"}]
        ignore = {"ignore_from": at("11:10")[0], "ignore_to": datetime(2026, 10, 5, 11, 14, 59)}
        attendance, door, _, _ = zk.group_punches(txns, DAY, DAY, {("1", DAY): ignore, ("15", DAY): dict(ignore)})
        self.assertEqual((attendance["1"].get(DAY), door["1"][DAY]), (None, [datetime(2026, 10, 5, 9, 31, 18)]))
        self.assertNotIn(DAY, attendance["15"])
        days = zk.build_days(attendance["1"], door["1"], today=date(2026, 10, 6))
        self.assertIn("aucun pointage sur la pointeuse intérieure", days[DAY]["anomaly"])

    def test_corrections_file_and_window(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.csv"
            path.write_text("numero;date;arrivee;depart;commentaire\n5;2026-10-05;08:00;;oubli\n"
                            "6;2026-10-01;07:55;;hors période\n", encoding="utf-8")
            corrections = zk.load_corrections(path)
        txns = [{"id": 1, "emp_code": "5", "punch_time": "2026-10-05 07:07:14", "terminal_sn": "INSIDE"}]
        attendance, _, _, _ = zk.group_punches(txns, DAY, DAY, corrections)
        self.assertEqual(attendance["5"][DAY], at("08:00"))
        self.assertNotIn(date(2026, 10, 1), attendance["6"])


class FakeOdoo:
    def __init__(self, records=()):
        self.records = {r["id"]: dict(r) for r in records}
        self.calls = []

    def call(self, model, method, *args, **kwargs):
        self.calls.append(method)
        if method == "search_read":
            return [dict(r) for r in self.records.values()]
        if method == "create":
            for vals in args[0]:
                new_id = max(self.records, default=0) + 1
                self.records[new_id] = {"id": new_id, **vals}
            return []
        if method == "write":
            for rid in args[0]:
                self.records[rid].update(args[1])
            return True
        raise AssertionError(method)


class SyncEmployeeTest(unittest.TestCase):
    FIELDS = {"pause_start": "x_studio_debut_pause", "pause_end": "x_studio_fin_pause", "hours": "x_studio_heures_travailles"}
    EMP = {"id": 7, "name": "Employé Test"}

    def days(self, *times, closed=True):
        return {DAY: zk.build_day(at(*times), closed=closed)}

    def test_create_then_update_then_idempotent(self):
        odoo = FakeOdoo()
        self.assertEqual(zk.sync_employee(odoo, self.EMP, self.days("08:00", closed=False), self.FIELDS), (1, 0))
        self.assertEqual(odoo.records[1]["check_out"], False)  # arrived, still at work
        self.assertEqual(zk.sync_employee(odoo, self.EMP, self.days("08:00", "12:30", closed=False), self.FIELDS), (0, 1))
        self.assertEqual((odoo.records[1]["check_out"], odoo.records[1]["x_studio_debut_pause"]),
                         (False, "2026-10-05 11:30:00"))  # out for lunch: pause in progress, not departure
        self.assertEqual(zk.sync_employee(odoo, self.EMP, self.days("08:00", "12:30", "13:30", "18:00"), self.FIELDS), (0, 1))
        rec = odoo.records[1]
        self.assertEqual((rec["x_studio_debut_pause"], rec["check_out"], rec["x_studio_heures_travailles"]),
                         ("2026-10-05 11:30:00", "2026-10-05 17:00:00", 9.0))
        self.assertEqual(zk.sync_employee(odoo, self.EMP, self.days("08:00", "12:30", "13:30", "18:00"), self.FIELDS), (0, 0))

    def test_several_records_same_day_untouched(self):
        odoo = FakeOdoo([{"id": 1, "check_in": "2026-10-05 07:00:00", "check_out": "2026-10-05 11:00:00"},
                         {"id": 2, "check_in": "2026-10-05 12:00:00", "check_out": "2026-10-05 17:00:00"}])
        self.assertEqual(zk.sync_employee(odoo, self.EMP, self.days("08:00", "18:00"), self.FIELDS), (0, 0))
        self.assertNotIn("write", odoo.calls)


if __name__ == "__main__":
    unittest.main()
