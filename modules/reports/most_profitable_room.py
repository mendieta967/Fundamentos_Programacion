from modules.rooms import get_room

from modules.helpers import show_room

from storage.json_storage import (
    load_reservations
)


def most_profitable_room():

    print("\n===== HABITACIÓN CON MAYOR INGRESO =====\n")

    reservations = load_reservations()

    if not reservations:

        print("No hay reservas registradas.")

        return

    rooms = {}

    for reservation in reservations:

        room_number = reservation["room_number"]

        if room_number in rooms:

            rooms[room_number] += reservation["total"]

        else:

            rooms[room_number] = reservation["total"]

    most_profitable = max(
        rooms,
        key=rooms.get
    )

    room = get_room(
        most_profitable
    )

    show_room(
        most_profitable,
        room
    )

    print(
        f"Ingresos generados: S/ {rooms[most_profitable]:.2f}"
    )