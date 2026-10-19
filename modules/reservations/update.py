from modules.validations import *
from storage.json_storage import *
from modules.rooms import *
from modules.payments import *


def select_reservation():

    customer_dni = custom_input(
        "Ingrese el DNI del cliente: "
    )

    if not validate_dni(customer_dni):

        print("DNI inválido.")

        return None, None, None

    reservations = load_reservations()

    customer_reservations = []

    for index, reservation in enumerate(reservations):

        if reservation["customer_dni"] == customer_dni:

            customer_reservations.append(
                (index, reservation)
            )

    if not customer_reservations:

        print("No se encontraron reservas.")

        return None, None, None

    print("\nReservas encontradas:\n")

    for option, (index, reservation) in enumerate(
        customer_reservations,
        start=1
    ):

        print(f"{option}. Habitación: {reservation['room_number']}")
        print(f"   Check-in: {reservation['check_in']}")
        print(f"   Check-out: {reservation['check_out']}")
        print(f"   Total: ${reservation['total']}")
        print("-" * 35)

    while True:

        selected = custom_input(
            "\nSeleccione una reserva: "
        )

        if selected.isdigit():

            selected = int(selected)

            if 1 <= selected <= len(customer_reservations):

                break

        print("Opción inválida.")

    reservation_index = customer_reservations[selected - 1][0]

    reservation = reservations[reservation_index]

    return reservations, reservation_index, reservation


def modify_reservation():

    print("\n===== MODIFICAR RESERVA =====\n")

    reservations, reservation_index, reservation = select_reservation()

    if reservations is None:

        return

    while True:

        print("\n¿Qué desea modificar?\n")

        print("1. Teléfono")
        print("2. Estadía")
        print("0. Cancelar")

        option = custom_input("\nSeleccione una opción: ")

        if option == "1":

            modify_phone(reservation)
            break

        elif option == "2":

            modify_stay(
                reservation,
                reservation_index
            )

            break

        elif option == "0":

            print("Modificación cancelada.")
            return

        else:

            print("Opción inválida.")

    save_reservations(reservations)

    print("\nReserva modificada correctamente.")


def modify_phone(reservation):

    while True:

        new_phone = custom_input(
            "Ingrese el nuevo teléfono: "
        )

        if validate_phone(new_phone):

            reservation["customer_phone"] = new_phone

            print("\nTeléfono actualizado correctamente.")

            return

        print(
            "Teléfono inválido. Debe contener 9 dígitos."
        )


def modify_stay(reservation, reservation_index):

    print("\n===== MODIFICAR ESTADÍA =====\n")

    while True:

        new_check_in = custom_input(
            "Ingrese el nuevo Check-in (dd/mm/yyyy): "
        )

        if not validate_date(new_check_in):

            print("Fecha inválida.")
            continue

        if not validate_future_date(new_check_in):

            print("La fecha debe ser hoy o futura.")
            continue

        break

    while True:

        new_check_out = custom_input(
            "Ingrese el nuevo Check-out (dd/mm/yyyy): "
        )

        if not validate_date(new_check_out):

            print("Fecha inválida.")
            continue

        nights = calculate_nights(
            new_check_in,
            new_check_out
        )

        if nights is None:

            print(
                "El Check-out debe ser posterior al Check-in."
            )

            continue

        break

    room_number = reservation["room_number"]

    if is_room_available_for_dates(
        room_number,
        new_check_in,
        new_check_out,
        reservation_index
    ):

        room = get_room(room_number)

    else:

        print(
            "\nLa habitación actual no está disponible para esas fechas."
        )

        room_number, room = select_room(
            reservation["guest_count"],
            new_check_in,
            new_check_out,
            reservation_index
        )

    subtotal = calculate_subtotal(
        room["price"],
        nights
    )

    igv = calculate_igv(subtotal)

    total = calculate_total(
        subtotal,
        igv
    )

    reservation["check_in"] = new_check_in
    reservation["check_out"] = new_check_out

    reservation["nights"] = nights

    reservation["room_number"] = room_number
    reservation["room_type"] = room["type"]

    reservation["subtotal"] = subtotal
    reservation["igv"] = igv
    reservation["total"] = total

    print("\nEstadía modificada correctamente.")