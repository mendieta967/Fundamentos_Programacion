from modules.payments import (
    calculate_igv,
    calculate_subtotal,
    calculate_total
)

from modules.rooms import (
    get_room,
    is_room_available_for_dates,
    select_room
)

from modules.validations import (
    calculate_nights,
    custom_input,
    validate_date,
    validate_dni,
    validate_future_date,
    validate_phone
)

from storage.json_storage import (
    get_customer_by_dni,
    load_customers,
    load_reservations,
    save_customers,
    save_reservations
)


# ==========================================
# SELECCIONAR RESERVA
# ==========================================

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

    print("\n===== RESERVAS ENCONTRADAS =====\n")

    for option, (index, reservation) in enumerate(
        customer_reservations,
        start=1
    ):

        print(f"{option}. Habitación: {reservation['room_number']}")
        print(f"   Tipo: {reservation['room_type']}")
        print(f"   Check-in: {reservation['check_in']}")
        print(f"   Check-out: {reservation['check_out']}")
        print(f"   Total: S/ {reservation['total']:.2f}")
        print("-" * 35)

    while True:

        selected = custom_input(
            "\nSeleccione una reserva: "
        )

        if (
            selected.isdigit()
            and
            1 <= int(selected) <= len(customer_reservations)
        ):

            reservation_index = customer_reservations[
                int(selected) - 1
            ][0]

            reservation = reservations[
                reservation_index
            ]

            return (
                reservations,
                reservation_index,
                reservation
            )

        print("Opción inválida.")


# ==========================================
# MODIFICAR RESERVA
# ==========================================

def modify_reservation():

    print("\n===== MODIFICAR RESERVA =====\n")

    reservations, reservation_index, reservation = (
        select_reservation()
    )

    if reservations is None:

        return

    while True:

        print("\n¿Qué desea modificar?\n")

        print("1. Datos del cliente")
        print("2. Estadía")
        print("0. Cancelar")

        option = custom_input(
            "\nSeleccione una opción: "
        )

        if option == "1":

            modify_customer(reservation)

            break

        elif option == "2":

            modify_stay(
                reservation,
                reservation_index
            )

            save_reservations(reservations)

            break

        elif option == "0":

            print("Modificación cancelada.")
            return

        else:

            print("Opción inválida.")

    print("\nDatos actualizados correctamente.")


# ==========================================
# MODIFICAR DATOS DEL CLIENTE
# ==========================================

def modify_customer(reservation):

    customers = load_customers()

    customer = get_customer_by_dni(
        reservation["customer_dni"]
    )

    while True:

        print("\n===== DATOS DEL CLIENTE =====\n")

        print("1. Modificar teléfono")
        print("0. Volver")

        option = custom_input(
            "\nSeleccione una opción: "
        )

        if option == "1":

            while True:

                new_phone = custom_input(
                    "Ingrese el nuevo teléfono: "
                )

                if validate_phone(new_phone):

                    customer["customer_phone"] = new_phone

                    save_customers(customers)

                    print(
                        "\nTeléfono actualizado correctamente."
                    )

                    return

                print(
                    "Teléfono inválido. Debe contener 9 dígitos."
                )

        elif option == "0":

            return

        else:

            print("Opción inválida.")


# ==========================================
# MODIFICAR ESTADÍA
# ==========================================

def modify_stay(
    reservation,
    reservation_index
):

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