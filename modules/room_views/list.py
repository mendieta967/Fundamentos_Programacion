from modules.helpers import show_room

from modules.rooms import rooms, get_room_current_reservation


def list_rooms():

    print("\n===== LISTA DE HABITACIONES =====\n")

    for room_number, room in rooms.items():

        show_room(
            room_number,
            room
        )

        reservation = get_room_current_reservation(
            room_number
        )

        if reservation:

            print("Estado: Ocupada")

        else:

            print("Estado: Disponible")

        print()