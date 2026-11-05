import unittest
from datetime import date, timedelta
from unittest.mock import patch

from frontend.components.services.edit_reservation_service import (
    rebook_cancelled_reservation,
    update_reservation
)


class CancelledReservationRebookingTests(unittest.TestCase):

    def setUp(self):
        check_in = date.today() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        self.cancelled_reservation = {
            "customer_dni": "95211565",
            "check_in": "03/11/2026",
            "check_out": "05/11/2026",
            "nights": 2,
            "guest_count": 2,
            "room_number": 303,
            "room_type": "Suite",
            "payment_method": "efectivo",
            "receipt_type": "boleta",
            "subtotal": 240,
            "igv": 43.2,
            "total": 283.2,
            "status": "cancelled",
        }
        self.rebook_check_in = check_in.strftime("%d/%m/%Y")
        self.rebook_check_out = check_out.strftime("%d/%m/%Y")
        self.reservations = [self.cancelled_reservation]
        self.selected_room = {
            "number": 201,
            "type": "Double",
            "price": 80,
            "capacity": 2,
        }

    def test_rebooking_preserves_cancelled_record_and_appends_active_reservation(self):
        original = dict(self.cancelled_reservation)
        with (
            patch(
                "frontend.components.services.edit_reservation_service.load_reservations",
                return_value=self.reservations
            ),
            patch(
                "frontend.components.services.edit_reservation_service.get_available_rooms",
                return_value=[self.selected_room]
            ) as get_available_rooms,
            patch(
                "frontend.components.services.edit_reservation_service.save_reservations"
            ) as save_reservations
        ):
            new_reservation = rebook_cancelled_reservation(
                0,
                self.rebook_check_in,
                self.rebook_check_out,
                2,
                201
            )

        self.assertEqual(self.reservations[0], original)
        self.assertEqual(new_reservation["status"], "active")
        self.assertEqual(new_reservation["customer_dni"], original["customer_dni"])
        self.assertEqual(new_reservation["room_number"], 201)
        self.assertEqual(new_reservation["room_type"], "Double")
        self.assertEqual(new_reservation["nights"], 2)
        self.assertEqual(new_reservation["subtotal"], 160)
        self.assertAlmostEqual(new_reservation["total"], 188.8)
        self.assertEqual(len(self.reservations), 2)
        get_available_rooms.assert_called_once_with(
            2,
            self.rebook_check_in,
            self.rebook_check_out
        )
        save_reservations.assert_called_once_with(self.reservations)

    def test_rebooking_rejects_unavailable_room_without_changing_history(self):
        original = dict(self.cancelled_reservation)
        with (
            patch(
                "frontend.components.services.edit_reservation_service.load_reservations",
                return_value=self.reservations
            ),
            patch(
                "frontend.components.services.edit_reservation_service.get_available_rooms",
                return_value=[]
            ),
            patch(
                "frontend.components.services.edit_reservation_service.save_reservations"
            ) as save_reservations
        ):
            with self.assertRaisesRegex(ValueError, "ya no está disponible"):
                rebook_cancelled_reservation(
                    0,
                    self.rebook_check_in,
                    self.rebook_check_out,
                    2,
                    201
                )

        self.assertEqual(self.reservations, [original])
        save_reservations.assert_not_called()

    def test_rebooking_does_not_allow_overlap_with_an_active_stay(self):
        active_reservation = {
            "customer_dni": "12365498",
            "check_in": self.rebook_check_in,
            "check_out": self.rebook_check_out,
            "nights": 2,
            "guest_count": 1,
            "room_number": 303,
            "room_type": "Suite",
            "total": 283.2,
            "status": "active",
        }
        reservations = [self.cancelled_reservation, active_reservation]
        rooms = {
            201: {
                "type": "Double",
                "capacity": 2,
                "price": 80,
                "maintenance": False,
            },
            303: {
                "type": "Suite",
                "capacity": 4,
                "price": 120,
                "maintenance": False,
            },
        }
        with (
            patch(
                "frontend.components.services.edit_reservation_service.load_reservations",
                return_value=reservations
            ),
            patch(
                "modules.rooms.load_reservations",
                return_value=reservations
            ),
            patch("modules.rooms.get_rooms", return_value=rooms),
            patch(
                "frontend.components.services.edit_reservation_service.save_reservations"
            ) as save_reservations
        ):
            with self.assertRaisesRegex(ValueError, "ya no está disponible"):
                rebook_cancelled_reservation(
                    0,
                    self.rebook_check_in,
                    self.rebook_check_out,
                    2,
                    303
                )

        self.assertEqual(len(reservations), 2)
        save_reservations.assert_not_called()

    def test_rebooking_requires_a_valid_future_or_today_check_in(self):
        past_check_in = (date.today() - timedelta(days=2)).strftime("%d/%m/%Y")
        past_check_out = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        with patch(
            "frontend.components.services.edit_reservation_service.load_reservations",
            return_value=self.reservations
        ):
            with self.assertRaisesRegex(ValueError, "Check In"):
                rebook_cancelled_reservation(
                    0,
                    past_check_in,
                    past_check_out,
                    2,
                    201
                )

    def test_rebooking_rejects_non_cancelled_reservation(self):
        active = dict(self.cancelled_reservation, status="active")
        with patch(
            "frontend.components.services.edit_reservation_service.load_reservations",
            return_value=[active]
        ):
            with self.assertRaisesRegex(ValueError, "ya no está cancelada"):
                rebook_cancelled_reservation(
                    0,
                    "06/11/2026",
                    "08/11/2026",
                    2,
                    201
                )

    def test_normal_edit_cannot_mutate_cancelled_history(self):
        with (
            patch(
                "frontend.components.services.edit_reservation_service.load_reservations",
                return_value=self.reservations
            ),
            patch(
                "frontend.components.services.edit_reservation_service.save_reservations"
            ) as save_reservations
        ):
            with self.assertRaisesRegex(ValueError, "no se puede editar"):
                update_reservation(
                    0,
                    self.rebook_check_in,
                    self.rebook_check_out,
                    2,
                    201
                )

        save_reservations.assert_not_called()
