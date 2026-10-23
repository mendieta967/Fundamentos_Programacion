from datetime import datetime

from modules.helpers import show_reservation

from storage.json_storage import (
    load_reservations
)


def today_reservations():

    print("\n===== RESERVAS DEL DÍA =====\n")

    reservations = load_reservations()

    today = datetime.today().strftime(
        "%d/%m/%Y"
    )

    has_reservations = False

    for reservation in reservations:

        if reservation["check_in"] == today:

            show_reservation(
                reservation
            )

            has_reservations = True

    if not has_reservations:

        print(
            "No hay reservas para el día de hoy."
        )