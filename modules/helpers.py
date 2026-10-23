from storage.json_storage import get_customer_by_dni


# ==========================================
# MOSTRAR RESERVA
# ==========================================

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

        print("Cliente no encontrado en el registro.")

    print()

    print(f"Habitación: {reservation['room_number']}")
    print(f"Tipo: {reservation['room_type']}")

    print()

    print(f"Check-in: {reservation['check_in']}")
    print(f"Check-out: {reservation['check_out']}")

    print(f"Huéspedes: {reservation['guest_count']}")

    print()

    print(f"Subtotal: S/ {reservation['subtotal']:.2f}")
    print(f"IGV: S/ {reservation['igv']:.2f}")
    print(f"Total: S/ {reservation['total']:.2f}")

    print()

    print(f"Método de pago: {reservation['payment_method']}")
    print(f"Comprobante: {reservation['receipt_type']}")


# ==========================================
# MOSTRAR CLIENTE
# ==========================================

def show_customer(customer):

    print("-" * 40)

    print(f"Nombre: {customer['customer_name']}")
    print(f"DNI: {customer['customer_dni']}")
    print(f"Teléfono: {customer['customer_phone']}")


# ==========================================
# MOSTRAR HABITACIÓN
# ==========================================

def show_room(room_number, room):

    print("-" * 40)

    print(f"Habitación: {room_number}")
    print(f"Tipo: {room['type']}")
    print(f"Capacidad: {room['capacity']}")
    print(f"Precio por noche: S/ {room['price']:.2f}")