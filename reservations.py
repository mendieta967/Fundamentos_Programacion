from rooms import *
from validations import *
from payments import *
from storage import *


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

def show_customer_reservations():

    customer_dni = custom_input(
        "Ingrese su DNI: "
    )


    if not validate_dni(customer_dni):

        print("DNI inválido.")

        return


    reservations = load_reservations()

    found_reservation = False


    print("\n===== MIS RESERVAS =====\n")


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
