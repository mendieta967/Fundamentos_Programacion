from modules.payments import calculate_igv, calculate_subtotal, calculate_total
from modules.reservation_status import cancel_reservation, restore_reservation
from modules.validations import calculate_nights
from frontend.components.services.customer_service import CustomerService
from storage.json_storage import (
    get_customer_by_dni,
    load_customers,
    load_reservations,
    save_customers,
    save_reservations
)


def build_reservation_data(
    customer_dni,
    check_in,
    check_out,
    guest_count,
    selected_room,
    payment_method,
    receipt_type
):
    nights = calculate_nights(check_in, check_out)
    subtotal = calculate_subtotal(selected_room["price"], nights)
    igv = calculate_igv(subtotal)

    return {
        "customer_dni": customer_dni,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "guest_count": guest_count,
        "room_number": selected_room["number"],
        "room_type": selected_room["type"],
        "payment_method": payment_method.lower(),
        "receipt_type": receipt_type.lower(),
        "subtotal": subtotal,
        "igv": igv,
        "total": calculate_total(subtotal, igv)
    }


def persist_reservation(customer, reservation):
    customer_dni = reservation["customer_dni"]
    existing_customer = get_customer_by_dni(customer_dni)
    if existing_customer is not None and not CustomerService.is_active(
        existing_customer
    ):
        raise ValueError(
            "El cliente está dado de baja. Restauralo antes de crear "
            "una nueva reserva."
        )

    if existing_customer is None:
        customers = load_customers()
        customers.append(customer)
        save_customers(customers)

    reservations = load_reservations()
    reservations.append(reservation)
    save_reservations(reservations)


__all__ = [
    "build_reservation_data",
    "cancel_reservation",
    "persist_reservation",
    "restore_reservation"
]