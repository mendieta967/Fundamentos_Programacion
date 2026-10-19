def show_reservation(reservation):

    print("-" * 40)

    print(f"Cliente: {reservation['customer_name']}")
    print(f"DNI: {reservation['customer_dni']}")
    print(f"Teléfono: {reservation['customer_phone']}")

    print(f"Habitación: {reservation['room_number']}")
    print(f"Tipo: {reservation['room_type']}")

    print(f"Check-in: {reservation['check_in']}")
    print(f"Check-out: {reservation['check_out']}")

    print(f"Huéspedes: {reservation['guest_count']}")

    print(f"Subtotal: S/ {reservation['subtotal']}")
    igv = reservation.get("igv", reservation.get("iva", 0))
    print(f"IGV: S/ {igv}")
    print(f"Total: S/ {reservation['total']}")

    print(f"Método de pago: {reservation['payment_method']}")
    print(f"Comprobante: {reservation['receipt_type']}")