from modules.rooms import room_exists, get_room, get_room_current_reservation

from modules.helpers import show_room


def search_room():

    print("\n===== BUSCAR HABITACIÓN =====\n")

    while True:

        room_number = input(
            "Ingrese el número de habitación: "
        )

        if not room_number.isdigit():

            print("Debe ingresar un número.")

            continue

        room_number = int(room_number)

        break

    if not room_exists(room_number):

        print("\nLa habitación no existe.")

        return

    room = get_room(room_number)

    reservation = get_room_current_reservation(
        room_number
    )

    print()

    show_room(
        room_number,
        room
    )

    print()

    if reservation:

        print("Estado: Ocupada\n")

        print(f"Cliente: {reservation['customer_name']}")
        print(f"Desde: {reservation['check_in']}")
        print(f"Hasta: {reservation['check_out']}")

    else:

        print("Estado: Disponible")