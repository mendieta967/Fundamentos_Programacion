from datetime import datetime

from modules.reservation_status import is_reservation_cancelled
from storage.json_storage import load_reservations


DATE_FORMAT = "%d/%m/%Y"


class ReservationSearchService:

    @staticmethod
    def search_by_dni(dni):

        reservations = load_reservations()

        return [
            reservation
            for reservation in reservations
            if reservation["customer_dni"] == dni
        ]

    @staticmethod
    def filter_reservations(
        reservations,
        room_query="",
        date_from="",
        date_to="",
        status="Todos los estados"
    ):
        room_query = room_query.strip().casefold()
        date_from_value = None
        date_to_value = None

        if date_from:
            date_from = date_from.strip()
            if len(date_from) != 10:
                date_from = ""
            else:
                date_from_value = datetime.strptime(date_from, DATE_FORMAT).date()
        if date_to:
            date_to = date_to.strip()
            if len(date_to) != 10:
                date_to = ""
            else:
                date_to_value = datetime.strptime(date_to, DATE_FORMAT).date()
        if date_from_value and date_to_value:
            if date_from_value > date_to_value:
                raise ValueError("La fecha Desde no puede ser posterior a Hasta.")

        today = datetime.today().date()
        filtered = []

        for original_index, reservation in enumerate(reservations):
            if room_query:
                room_number = str(reservation.get("room_number", ""))
                if room_query not in room_number.casefold():
                    continue

            check_in = datetime.strptime(
                reservation["check_in"], DATE_FORMAT
            ).date()
            check_out = datetime.strptime(
                reservation["check_out"], DATE_FORMAT
            ).date()

            if date_from_value and check_out <= date_from_value:
                continue
            if date_to_value and check_in > date_to_value:
                continue

            if is_reservation_cancelled(reservation):
                reservation_status = "Cancelada"
            elif check_out < today:
                reservation_status = "Finalizada"
            else:
                reservation_status = "Activa"

            if status != "Todos los estados" and reservation_status != status:
                continue

            filtered.append((original_index, reservation, reservation_status))

        return filtered


def normalized_room_query(room_number):
    return room_number.casefold()
