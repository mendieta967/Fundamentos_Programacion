import unittest
from datetime import date, datetime
from unittest.mock import patch

from modules.reports.report_data import get_report_data
from modules.rooms import get_room_current_reservation


class ReportDataTests(unittest.TestCase):

    def setUp(self):
        self.reservations = [
            {
                "customer_dni": "111",
                "check_in": "05/11/2026",
                "check_out": "07/11/2026",
                "room_number": 101,
                "guest_count": 2,
                "total": 150,
            },
            {
                "customer_dni": "111",
                "check_in": "03/11/2026",
                "check_out": "05/11/2026",
                "room_number": 101,
                "guest_count": 1,
                "total": 100,
            },
            {
                "customer_dni": "222",
                "check_in": "05/11/2026",
                "check_out": "06/11/2026",
                "room_number": 103,
                "guest_count": 1,
                "total": 100,
            },
            {
                "customer_dni": "222",
                "check_in": "05/11/2026",
                "check_out": "06/11/2026",
                "room_number": 102,
                "guest_count": 4,
                "total": 999,
                "status": "cancelled",
            },
        ]
        self.customers = [
            {"customer_dni": "111", "customer_name": "Ana"},
            {"customer_dni": "222", "customer_name": "Beto"},
        ]
        self.rooms = {
            101: {"type": "Doble", "maintenance": False},
            102: {"type": "Suite", "maintenance": True},
            103: {"type": "Simple", "maintenance": False},
        }

    def get_report(self, report_key, reservations=None):
        source_reservations = (
            self.reservations if reservations is None else reservations
        )
        with (
            patch(
                "modules.reports.report_data.load_reservations",
                return_value=source_reservations
            ),
            patch(
                "modules.reports.report_data.load_customers",
                return_value=self.customers
            ),
            patch(
                "modules.reports.report_data.get_rooms",
                return_value=self.rooms
            )
        ):
            return get_report_data(report_key, date(2026, 11, 5))

    def test_today_report_excludes_cancelled_and_checkout_day(self):
        report = self.get_report("today")

        self.assertEqual(len(report["rows"]), 2)
        self.assertEqual(report["metrics"][0][1], "2")
        self.assertEqual(report["metrics"][1][1], "3")
        self.assertNotIn("102", [row[2] for row in report["rows"]])

    def test_frequent_customers_are_ordered_by_active_reservation_count(self):
        report = self.get_report("frequent_customers")

        self.assertEqual(
            report["rows"],
            [("Ana", "111", "2"), ("Beto", "222", "1")]
        )

    def test_room_demand_and_income_exclude_cancelled_reservations(self):
        demand = self.get_report("most_reserved_room")
        income = self.get_report("room_income")

        self.assertEqual(demand["rows"][0], ("101", "Doble", "2"))
        room_income = {
            row[0]: row[2]
            for row in income["rows"]
        }
        self.assertEqual(room_income["101"], "S/ 250.00")
        self.assertEqual(room_income["102"], "S/ 0.00")

    def test_total_income_includes_average_and_active_reservation_count(self):
        report = self.get_report("total_income")

        self.assertEqual(
            [metric[1] for metric in report["metrics"]],
            ["S/ 350.00", "3", "S/ 116.67"]
        )

    def test_occupancy_uses_half_open_stay_dates_and_excludes_maintenance(self):
        report = self.get_report("occupancy")

        self.assertEqual(
            [metric[1] for metric in report["metrics"]],
            ["100 %", "2", "0", "1"]
        )
        self.assertEqual(report["rows"][0][2], "Ocupada")
        self.assertEqual(report["rows"][1][2], "Mantenimiento")
        self.assertEqual(report["rows"][2][2], "Ocupada")

    def test_empty_income_report_has_zero_totals(self):
        report = self.get_report("total_income", reservations=[])

        self.assertEqual(
            [metric[1] for metric in report["metrics"]],
            ["S/ 0.00", "0", "S/ 0.00"]
        )
        self.assertEqual(report["rows"], [])

    def test_unknown_report_fails_explicitly(self):
        with self.assertRaises(ValueError):
            self.get_report("unknown")


class CurrentRoomReservationTests(unittest.TestCase):

    def test_check_out_date_is_not_treated_as_occupied(self):
        class FixedDateTime:
            @staticmethod
            def today():
                return datetime(2026, 11, 5)

            strptime = staticmethod(datetime.strptime)

        reservations = [
            {
                "room_number": 101,
                "check_in": "03/11/2026",
                "check_out": "05/11/2026",
            },
            {
                "room_number": 103,
                "check_in": "05/11/2026",
                "check_out": "06/11/2026",
            },
            {
                "room_number": 102,
                "check_in": "05/11/2026",
                "check_out": "06/11/2026",
                "status": "cancelled",
            },
        ]
        with (
            patch("modules.rooms.datetime", FixedDateTime),
            patch("modules.rooms.load_reservations", return_value=reservations)
        ):
            self.assertIsNone(get_room_current_reservation(101))
            self.assertIs(
                get_room_current_reservation(103),
                reservations[1]
            )
            self.assertIsNone(get_room_current_reservation(102))
