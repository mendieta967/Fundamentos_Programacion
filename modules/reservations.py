from .rooms import *
from .validations import *
from .payments import *
from storage.json_storage import *

def reservations_menu():

    while True:

        print("\n===== GESTIÓN DE RESERVAS =====\n")

        print("1. Registrar reserva")
        print("2. Ver reservas")
        print("3. Modificar reserva")
        print("4. Eliminar reserva")
        print("5. Buscar reserva")
        print("6. Ordenar reservas")
        print("0. Volver")

        option = input("\nSeleccione una opción: ")

        if option == "1":
            create_reservation()

        elif option == "2":
            show_reservations_by_dni()

        elif option == "3":
            modify_reservation()

        elif option == "4":
            delete_reservation()

        elif option == "5":
            print("Función en desarrollo.")

        elif option == "6":
            print("Función en desarrollo.")

        elif option == "0":
            break

        else:
            print("Opción inválida.")

def create_reservation():

    print("===== CREAR RESERVA =====\n")
    print("Escriba 'cancelar' en cualquier momento para salir.\n")


    # ==============================
    # VALIDAR NOMBRE
    # ==============================

    while True:

        customer_name = custom_input("Ingrese su nombre y apellido: ")

        if validate_name(customer_name):

            break

        print("Nombre inválido. Intente nuevamente.")


   # ==============================
# VALIDAR DNI
# ==============================

    while True:

        customer_dni = custom_input("Ingrese su DNI: ")

        if validate_dni(customer_dni):

            break

        print("DNI inválido. Debe contener 8 dígitos numéricos.")


    # ==============================
    # VALIDAR SI EL CLIENTE YA TIENE RESERVAS
    # ==============================

    if customer_has_reservations(customer_dni):

        print("\nEl cliente ya tiene reservas registradas.")

        while True:

            continue_reservation = custom_input(
                "¿Desea realizar otra reserva? (s/n): "
            ).lower()

            if continue_reservation in ["s", "n"]:

                break

            print("Opción inválida.")


        if continue_reservation == "n":

            print("Reserva cancelada. Gracias por visitarnos.")

            return
    # ==============================
    # VALIDAR TELÉFONO
    # ==============================

    while True:

        customer_phone = custom_input("Ingrese su número de teléfono: ")

        if validate_phone(customer_phone):

            break

        print("Teléfono inválido. Debe contener 9 dígitos numéricos.")


    # ==============================
    # VALIDAR CHECK-IN
    # ==============================

    while True:

        check_in = custom_input("Ingrese fecha de entrada (dd/mm/yyyy): ")

        if validate_date(check_in) and validate_future_date(check_in):

            break

        print("Fecha inválida o anterior a la fecha actual.")


    # ==============================
    # VALIDAR CHECK-OUT
    # ==============================

    while True:

        check_out = custom_input("Ingrese fecha de salida (dd/mm/yyyy): ")

        if not validate_date(check_out):

            print("Fecha inválida. Use el formato dd/mm/yyyy.")

            continue


        nights = calculate_nights(check_in, check_out)

        if nights is None:

            print("La fecha de salida debe ser posterior a la fecha de entrada.")

            continue

        break


    # ==============================
    # VALIDAR HUÉSPEDES
    # ==============================

    while True:

        guest_count = custom_input("Ingrese cantidad de huéspedes: ")

        if validate_guest_count(guest_count):

            guest_count = int(guest_count)

            break

        print("Cantidad inválida. Debe ser entre 1 y 4.")


    # ==============================
    # MOSTRAR HABITACIONES
    # ==============================

    show_available_rooms(guest_count,check_in,check_out)


    # ==============================
    # SELECCIONAR HABITACIÓN
    # ==============================

    while True:

        room_number = custom_input("Seleccione una habitación: ")


        # Validar número
        if not room_number.isdigit():

            print("Debe ingresar un número de habitación.")

            continue


        room_number = int(room_number)


        # Validar existencia
        if not room_exists(room_number):

            print("La habitación no existe.")

            continue


        # Validar disponibilidad
        if not is_room_available_for_dates(
            room_number,
            check_in,
            check_out
        ):

            print("La habitación ya está reservada para esas fechas.")

            continue


        # Obtener habitación
        room = get_room(room_number)


        # Validar capacidad
        if room["capacity"] < guest_count:

            print("La habitación no soporta esa cantidad de huéspedes.")

            continue


        break


    # ==============================
    # CALCULAR SUBTOTAL
    # ==============================

    subtotal = calculate_subtotal(room["price"], nights)


    # ==============================
    # MÉTODO DE PAGO
    # ==============================

    while True:

        payment_method = custom_input(
            "Método de pago (Efectivo/Tarjeta/Transferencia): "
        ).lower()

        if payment_method in [
            "efectivo",
            "tarjeta",
            "transferencia"
        ]:

            break

        print(
            "Método inválido. Use "
            "'Efectivo', 'Tarjeta' o 'Transferencia'."
        )


    # ==============================
    # IVA Y TOTAL
    # ==============================

    iva = calculate_iva(subtotal, payment_method)

    total = calculate_total(subtotal, iva)


    # ==============================
    # COMPROBANTE
    # ==============================

    while True:

        receipt_type = custom_input(
            "Tipo de comprobante (boleta/factura): "
        ).lower()

        if receipt_type in ["boleta", "factura"]:

            break

        print("Tipo de comprobante inválido.")


    # ==============================
    # RESUMEN FINAL
    # ==============================

    print("\n===== RESUMEN DE RESERVA =====")

    print(f"Comprobante: {receipt_type}")

    print(f"Cliente: {customer_name}")
    print(f"DNI: {customer_dni}")
    print(f"Teléfono: {customer_phone}")

    print(f"\nCheck-in: {check_in}")
    print(f"Check-out: {check_out}")

    print(f"Noches: {nights}")
    print(f"Huéspedes: {guest_count}")

    print(f"\nHabitación: {room_number}")
    print(f"Tipo: {room['type']}")
    print(f"Precio por noche: ${room['price']}")

    print(f"\nSubtotal: ${subtotal}")
    print(f"IVA: ${iva}")
    print(f"TOTAL: ${total}")

    print("\n¡Reserva realizada con éxito!")


    # ==============================
    # GUARDAR RESERVA
    # ==============================

    reservation_data = {

        "customer_name": customer_name,
        "customer_dni": customer_dni,
        "customer_phone": customer_phone,

        "check_in": check_in,
        "check_out": check_out,

        "nights": nights,
        "guest_count": guest_count,

        "room_number": room_number,
        "room_type": room["type"],

        "payment_method": payment_method,
        "receipt_type": receipt_type,

        "subtotal": subtotal,
        "iva": iva,
        "total": total
    }


    reservations = load_reservations()

    reservations.append(reservation_data)

    save_reservations(reservations)

def show_reservations_by_dni():

    customer_dni = custom_input(
        "Ingrese su DNI: "
    )


    if not validate_dni(customer_dni):

        print("DNI inválido.")

        return


    reservations = load_reservations()

    found_reservation = False


    print("\n===== RESERVAS =====\n")


    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            found_reservation = True

            print(f"Cliente: {reservation['customer_name']}")

            print(f"Habitación: {reservation['room_number']}")

            print(f"Tipo: {reservation['room_type']}")

            print(f"Check-in: {reservation['check_in']}")

            print(f"Check-out: {reservation['check_out']}")

            print(f"Total: ${reservation['total']}")

            print("-" * 35)


    if not found_reservation:

        print("No se encontraron reservas para ese DNI.")

def modify_reservation():

    print("\n===== MODIFICAR RESERVA =====\n")

    customer_dni = custom_input("Ingrese el DNI del cliente: ")

    if not validate_dni(customer_dni):

        print("DNI inválido.")
        return

    reservations = load_reservations()

    customer_reservations = []

    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            customer_reservations.append(reservation)

    if len(customer_reservations) == 0:

        print("\nNo se encontraron reservas para ese cliente.")
        return

    print("\nReservas encontradas:\n")

    for index, reservation in enumerate(customer_reservations, start=1):

        print(f"{index}. Habitación: {reservation['room_number']}")
        print(f"   Check-in: {reservation['check_in']}")
        print(f"   Check-out: {reservation['check_out']}")
        print(f"   Total: ${reservation['total']}")
        print("-" * 35)

    while True:

        option = input("\nSeleccione la reserva a modificar: ")

        if option.isdigit():

            option = int(option)

            if 1 <= option <= len(customer_reservations):

                break

        print("Opción inválida.")

    show_reservation(selected_reservation)

    while True:

        print("\n===== EDITAR RESERVA =====\n")

        print("1. Modificar Check-in")
        print("2. Modificar Check-out")
        print("3. Modificar cantidad de huéspedes")
        print("4. Modificar habitación")
        print("5. Modificar método de pago")
        print("6. Modificar comprobante")
        print("7. Ver datos actuales")
        print("0. Guardar cambios")

        option = input("\nSeleccione una opción: ")

        if option == "1":

            modify_check_in(selected_reservation)

        elif option == "2":

            modify_check_out(selected_reservation)

        elif option == "3":

            modify_guest_count(selected_reservation)

        elif option == "4":

            modify_room(selected_reservation)

        elif option == "5":

            modify_payment_method(selected_reservation)

        elif option == "6":

            modify_receipt(selected_reservation)

        elif option == "7":

            show_reservation(selected_reservation)

        elif option == "0":

            save_reservations(reservations)

            print("\nReserva modificada correctamente.")

            break

        else:

            print("Opción inválida.")

def show_reservation(reservation):

    print("\n===== DATOS DE LA RESERVA =====\n")

    print(f"Cliente: {reservation['customer_name']}")
    print(f"DNI: {reservation['customer_dni']}")
    print(f"Teléfono: {reservation['customer_phone']}")

    print(f"\nHabitación: {reservation['room_number']}")
    print(f"Tipo: {reservation['room_type']}")

    print(f"\nCheck-in: {reservation['check_in']}")
    print(f"Check-out: {reservation['check_out']}")
    print(f"Noches: {reservation['nights']}")
    print(f"Huéspedes: {reservation['guest_count']}")

    print(f"\nMétodo de pago: {reservation['payment_method']}")
    print(f"Comprobante: {reservation['receipt_type']}")

    print(f"\nSubtotal: ${reservation['subtotal']}")
    print(f"IVA: ${reservation['iva']}")
    print(f"TOTAL: ${reservation['total']}")

def modify_check_in(reservation):

    print("\n===== MODIFICAR CHECK-IN =====\n")

    print(f"Check-in actual: {reservation['check_in']}")

    while True:

        new_check_in = custom_input(
            "Nuevo Check-in (dd/mm/yyyy): "
        )

        if validate_date(new_check_in) and validate_future_date(new_check_in):

            break

        print("Fecha inválida.")

    nights = calculate_nights(
        new_check_in,
        reservation["check_out"]
    )

    if nights is None:

        print(
            "La nueva fecha debe ser anterior al Check-out."
        )

        return

    reservation["check_in"] = new_check_in
    reservation["nights"] = nights

    subtotal = calculate_subtotal(
        get_room(reservation["room_number"])["price"],
        nights
    )

    iva = calculate_iva(
        subtotal,
        reservation["payment_method"]
    )

    total = calculate_total(
        subtotal,
        iva
    )

    reservation["subtotal"] = subtotal
    reservation["iva"] = iva
    reservation["total"] = total

    print("\nCheck-in actualizado correctamente.")

def modify_check_out(reservation):

    print("\n===== MODIFICAR CHECK-OUT =====\n")

    print(f"Check-out actual: {reservation['check_out']}")

    while True:

        new_check_out = custom_input(
            "Nuevo Check-out (dd/mm/yyyy): "
        )

        if not validate_date(new_check_out):

            print("Fecha inválida.")
            continue

        nights = calculate_nights(
            reservation["check_in"],
            new_check_out
        )

        if nights is None:

            print(
                "La fecha debe ser posterior al Check-in."
            )

            continue

        break

    reservation["check_out"] = new_check_out
    reservation["nights"] = nights

    room = get_room(reservation["room_number"])

    subtotal = calculate_subtotal(
        room["price"],
        nights
    )

    iva = calculate_iva(
        subtotal,
        reservation["payment_method"]
    )

    total = calculate_total(
        subtotal,
        iva
    )

    reservation["subtotal"] = subtotal
    reservation["iva"] = iva
    reservation["total"] = total

    print("\nCheck-out actualizado correctamente.")

def modify_guest_count(reservation):

    print("\n===== MODIFICAR HUÉSPEDES =====\n")

    print(f"Huéspedes actuales: {reservation['guest_count']}")

    while True:

        guest_count = custom_input(
            "Nueva cantidad de huéspedes: "
        )

        if validate_guest_count(guest_count):

            guest_count = int(guest_count)

            break

        print("Cantidad inválida. Debe ser entre 1 y 4.")

    room = get_room(reservation["room_number"])

    # Si la habitación actual soporta la nueva cantidad,
    # solamente actualizamos el dato.
    if room["capacity"] >= guest_count:

        reservation["guest_count"] = guest_count

        print("\nCantidad de huéspedes actualizada.")

        return

    print(
        "\nLa habitación actual no tiene capacidad suficiente."
    )

    print(
        "Debe seleccionar una nueva habitación.\n"
    )

    show_available_rooms(
        guest_count,
        reservation["check_in"],
        reservation["check_out"]
    )

    while True:

        room_number = custom_input(
            "Seleccione una nueva habitación: "
        )

        if not room_number.isdigit():

            print("Debe ingresar un número.")

            continue

        room_number = int(room_number)

        if not room_exists(room_number):

            print("La habitación no existe.")

            continue

        if not is_room_available_for_dates(
            room_number,
            reservation["check_in"],
            reservation["check_out"]
        ):

            print(
                "La habitación está ocupada."
            )

            continue

        room = get_room(room_number)

        if room["capacity"] < guest_count:

            print(
                "La habitación no soporta esa cantidad."
            )

            continue

        break

    reservation["guest_count"] = guest_count
    reservation["room_number"] = room_number
    reservation["room_type"] = room["type"]

    subtotal = calculate_subtotal(
        room["price"],
        reservation["nights"]
    )

    iva = calculate_iva(
        subtotal,
        reservation["payment_method"]
    )

    total = calculate_total(
        subtotal,
        iva
    )

    reservation["subtotal"] = subtotal
    reservation["iva"] = iva
    reservation["total"] = total

    print("\nReserva actualizada correctamente.")

def modify_room(reservation):

    print("\n===== MODIFICAR HABITACIÓN =====\n")

    print(f"Habitación actual: {reservation['room_number']}")

    show_available_rooms(
        reservation["guest_count"],
        reservation["check_in"],
        reservation["check_out"]
    )

    while True:

        room_number = custom_input(
            "Seleccione la nueva habitación: "
        )

        if not room_number.isdigit():

            print("Debe ingresar un número.")

            continue

        room_number = int(room_number)

        if not room_exists(room_number):

            print("La habitación no existe.")

            continue

        if room_number == reservation["room_number"]:

            print("Esa ya es la habitación actual.")

            continue

        if not is_room_available_for_dates(
            room_number,
            reservation["check_in"],
            reservation["check_out"]
        ):

            print("La habitación está ocupada.")

            continue

        room = get_room(room_number)

        if room["capacity"] < reservation["guest_count"]:

            print(
                "La habitación no soporta esa cantidad de huéspedes."
            )

            continue

        break

    reservation["room_number"] = room_number
    reservation["room_type"] = room["type"]

    subtotal = calculate_subtotal(
        room["price"],
        reservation["nights"]
    )

    iva = calculate_iva(
        subtotal,
        reservation["payment_method"]
    )

    total = calculate_total(
        subtotal,
        iva
    )

    reservation["subtotal"] = subtotal
    reservation["iva"] = iva
    reservation["total"] = total

    print("\nHabitación modificada correctamente.")

def recalculate_reservation(reservation):

    room = get_room(reservation["room_number"])

    subtotal = calculate_subtotal(
        room["price"],
        reservation["nights"]
    )

    iva = calculate_iva(
        subtotal,
        reservation["payment_method"]
    )

    total = calculate_total(
        subtotal,
        iva
    )

    reservation["subtotal"] = subtotal
    reservation["iva"] = iva
    reservation["total"] = total

def modify_room(reservation):

    print("\n===== MODIFICAR HABITACIÓN =====\n")

    print(f"Habitación actual: {reservation['room_number']}")

    show_available_rooms(
        reservation["guest_count"],
        reservation["check_in"],
        reservation["check_out"]
    )

    while True:

        room_number = custom_input(
            "Seleccione la nueva habitación: "
        )

        if not room_number.isdigit():

            print("Debe ingresar un número.")

            continue

        room_number = int(room_number)

        if not room_exists(room_number):

            print("La habitación no existe.")

            continue

        if room_number == reservation["room_number"]:

            print("Esa ya es la habitación actual.")

            continue

        if not is_room_available_for_dates(
            room_number,
            reservation["check_in"],
            reservation["check_out"]
        ):

            print("La habitación está ocupada.")

            continue

        room = get_room(room_number)

        if room["capacity"] < reservation["guest_count"]:

            print("La habitación no soporta esa cantidad.")

            continue

        reservation["room_number"] = room_number
        reservation["room_type"] = room["type"]

        recalculate_reservation(reservation)

        print("\nHabitación modificada correctamente.")

        break
def modify_guest_count(reservation):

    print("\n===== MODIFICAR HUÉSPEDES =====\n")

    print(f"Huéspedes actuales: {reservation['guest_count']}")

    while True:

        guest_count = custom_input(
            "Nueva cantidad de huéspedes: "
        )

        if validate_guest_count(guest_count):

            guest_count = int(guest_count)

            break

        print("Cantidad inválida.")

    room = get_room(reservation["room_number"])

    if room["capacity"] >= guest_count:

        reservation["guest_count"] = guest_count

        print("\nCantidad de huéspedes actualizada.")

        return

    print("\nLa habitación actual no tiene capacidad suficiente.")

    show_available_rooms(
        guest_count,
        reservation["check_in"],
        reservation["check_out"]
    )

    while True:

        room_number = custom_input(
            "Seleccione una nueva habitación: "
        )

        if not room_number.isdigit():

            print("Debe ingresar un número.")

            continue

        room_number = int(room_number)

        if not room_exists(room_number):

            print("La habitación no existe.")

            continue

        if not is_room_available_for_dates(
            room_number,
            reservation["check_in"],
            reservation["check_out"]
        ):

            print("La habitación está ocupada.")

            continue

        room = get_room(room_number)

        if room["capacity"] < guest_count:

            print("La habitación no soporta esa cantidad.")

            continue

        reservation["guest_count"] = guest_count
        reservation["room_number"] = room_number
        reservation["room_type"] = room["type"]

        recalculate_reservation(reservation)

        print("\nReserva actualizada correctamente.")

        break
def delete_reservation():

    print("\n===== ELIMINAR RESERVA =====\n")

    customer_dni = custom_input(
        "Ingrese el DNI del cliente: "
    )

    if not validate_dni(customer_dni):

        print("DNI inválido.")
        return

    reservations = load_reservations()

    customer_reservations = []

    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            customer_reservations.append(reservation)

    if len(customer_reservations) == 0:

        print("\nNo se encontraron reservas.")
        return

    print("\nReservas encontradas:\n")

    for index, reservation in enumerate(customer_reservations, start=1):

        print(f"{index}. Habitación: {reservation['room_number']}")
        print(f"   Check-in: {reservation['check_in']}")
        print(f"   Check-out: {reservation['check_out']}")
        print(f"   Total: ${reservation['total']}")
        print("-" * 35)

    while True:

        option = custom_input(
            "Seleccione la reserva a eliminar: "
        )

        if option.isdigit():

            option = int(option)

            if 1 <= option <= len(customer_reservations):

                break

        print("Opción inválida.")

    reservation = customer_reservations[option - 1]

    confirmation = custom_input(
        "¿Está seguro? (s/n): "
    ).lower()

    if confirmation != "s":

        print("\nOperación cancelada.")
        return

    reservations.remove(reservation)

    save_reservations(reservations)

    print("\nReserva eliminada correctamente.")