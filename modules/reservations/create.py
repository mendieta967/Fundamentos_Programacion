from modules.rooms import *
from modules.validations import *
from modules.payments import *
from storage.json_storage import *


def create_reservation():

    print("===== CREAR RESERVA =====\n")
    print("Escriba 'cancelar' en cualquier momento para salir.\n")

    # ==============================
    # VALIDAR DNI
    # ==============================

    while True:

        customer_dni = custom_input("Ingrese su DNI: ")

        if validate_dni(customer_dni):

            break

        print("DNI inválido. Debe contener 8 dígitos numéricos.")

    # ==============================
    # VALIDAR SI EL CLIENTE YA EXISTE
    # ==============================

    new_customer = False

    if customer_exists(customer_dni):

        print("\nEl cliente ya se encuentra registrado.")

        while True:

            continue_reservation = custom_input(
                "¿Desea realizar una nueva reserva? (s/n): "
            ).lower()

            if continue_reservation in ["s", "n"]:

                break

            print("Opción inválida.")

        if continue_reservation == "n":

            print("Reserva cancelada. Gracias por visitarnos.")

            return

        customer = get_customer_by_dni(customer_dni)

        customer_name = customer["customer_name"]
        customer_phone = customer["customer_phone"]

    else:

        new_customer = True

        # ==============================
        # VALIDAR NOMBRE
        # ==============================

        while True:

            customer_name = custom_input(
                "Ingrese su nombre y apellido: "
            )

            if validate_name(customer_name):

                break

            print("Nombre inválido. Intente nuevamente.")

        # ==============================
        # VALIDAR TELÉFONO
        # ==============================

        while True:

            customer_phone = custom_input(
                "Ingrese su número de teléfono: "
            )

            if validate_phone(customer_phone):

                break

            print(
                "Teléfono inválido. Debe contener 9 dígitos numéricos."
            )

    # ==============================
    # VALIDAR CHECK-IN
    # ==============================

    while True:

        check_in = custom_input(
            "Ingrese fecha de entrada (dd/mm/yyyy): "
        )

        if validate_date(check_in) and validate_future_date(check_in):

            break

        print("Fecha inválida o anterior a la fecha actual.")

    # ==============================
    # VALIDAR CHECK-OUT
    # ==============================

    while True:

        check_out = custom_input(
            "Ingrese fecha de salida (dd/mm/yyyy): "
        )

        if not validate_date(check_out):

            print("Fecha inválida. Use el formato dd/mm/yyyy.")

            continue

        nights = calculate_nights(
            check_in,
            check_out
        )

        if nights is None:

            print(
                "La fecha de salida debe ser posterior a la fecha de entrada."
            )

            continue

        break

    # ==============================
    # VALIDAR HUÉSPEDES
    # ==============================

    while True:

        guest_count = custom_input(
            "Ingrese cantidad de huéspedes: "
        )

        if validate_guest_count(guest_count):

            guest_count = int(guest_count)

            break

        print("Cantidad inválida. Debe ser entre 1 y 4.")

    # ==============================
    # SELECCIONAR HABITACIÓN
    # ==============================

    room_number, room = select_room(
        guest_count,
        check_in,
        check_out
    )

    # ==============================
    # CALCULAR SUBTOTAL
    # ==============================

    subtotal = calculate_subtotal(
        room["price"],
        nights
    )

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
    # IGV Y TOTAL
    # ==============================

    igv = calculate_igv(subtotal)

    total = calculate_total(
        subtotal,
        igv
    )

    # ==============================
    # COMPROBANTE
    # ==============================

    while True:

        receipt_type = custom_input(
            "Tipo de comprobante (boleta/factura): "
        ).lower()

        if receipt_type in [
            "boleta",
            "factura"
        ]:

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
    print(f"Precio por noche: S/ {room['price']}")

    print(f"\nSubtotal: S/ {subtotal}")
    print(f"IGV: S/ {igv}")
    print(f"TOTAL: S/ {total}")

    print("\n¡Reserva realizada con éxito!")

    # ==============================
    # GUARDAR CLIENTE (SI ES NUEVO)
    # ==============================

    if new_customer:

        customers = load_customers()

        customer_data = {

            "customer_name": customer_name,
            "customer_dni": customer_dni,
            "customer_phone": customer_phone

        }

        customers.append(customer_data)

        save_customers(customers)

    # ==============================
    # GUARDAR RESERVA
    # ==============================

    reservation_data = {

        "customer_dni": customer_dni,

        "check_in": check_in,
        "check_out": check_out,

        "nights": nights,
        "guest_count": guest_count,

        "room_number": room_number,
        "room_type": room["type"],

        "payment_method": payment_method,
        "receipt_type": receipt_type,

        "subtotal": subtotal,
        "igv": igv,
        "total": total

    }

    reservations = load_reservations()

    reservations.append(reservation_data)

    save_reservations(reservations)