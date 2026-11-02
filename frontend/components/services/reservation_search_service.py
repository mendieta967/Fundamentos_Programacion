from storage.json_storage import load_reservations


class ReservationSearchService:

    @staticmethod
    def search_by_dni(dni):

        reservations = load_reservations()

        return [
            reservation
            for reservation in reservations
            if reservation["customer_dni"] == dni
        ]