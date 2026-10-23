from modules.rooms import get_room

from modules.helpers import show_room

from storage.json_storage import (
    load_reservations
)


def most_reserved_room():

    print("\n===== HABITACIÓN MÁS RESERVADA =====\n")

    reservations = load_reservations()

    if not reservations:

        print("No hay reservas registradas.")

        return

    rooms = {}

    for reservation in reservations:

        room_number = reservation["room_number"]

        if room_number in rooms:

            rooms[room_number] += 1

        else:

            rooms[room_number] = 1

    most_reserved = max(
        rooms,
        key=rooms.get
    )

    room = get_room(
        most_reserved
    )

    show_room(
        most_reserved,
        room
    )

    print(
        f"Cantidad de reservas: {rooms[most_reserved]}"
    )