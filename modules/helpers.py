from storage.json_storage import get_customer_by_dni


def show_reservation(reservation):

    customer = get_customer_by_dni(
        reservation["customer_dni"]
    )

    print("-" * 40)

    if customer:

        print(f"Cliente: {customer['customer_name']}")
        print(f"DNI: {customer['customer_dni']}")
        print(f"Teléfono: {customer['customer_phone']}")

    else:

        print("Cliente no encontrado.")

    print(f"Habitación: {reservation['room_number']}")
    print(f"Tipo: {reservation['room_type']}")

    print(f"Check-in: {reservation['check_in']}")
    print(f"Check-out: {reservation['check_out']}")

    print(f"Huéspedes: {reservation['guest_count']}")

    print(f"Subtotal: S/ {reservation['subtotal']}")
    print(f"IGV: S/ {reservation['igv']}")
    print(f"Total: S/ {reservation['total']}")

    print(f"Método de pago: {reservation['payment_method']}")
    print(f"Comprobante: {reservation['receipt_type']}")


def show_customer(customer):

    print("-" * 40)

    print(f"Nombre: {customer['customer_name']}")
    print(f"DNI: {customer['customer_dni']}")
    print(f"Teléfono: {customer['customer_phone']}")