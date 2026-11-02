from modules.payments import calculate_igv, calculate_subtotal, calculate_total
from modules.rooms import get_available_rooms
from modules.validations import calculate_nights
from storage.json_storage import load_reservations, save_reservations


def update_reservation(
    reservation_index,
    check_in,
    check_out,
    guest_count,
    room_number
):
    reservations = load_reservations()
    if not 0 <= reservation_index < len(reservations):
        raise IndexError("La reserva ya no existe.")

    available_rooms = get_available_rooms(
        guest_count,
        check_in,
        check_out,
        ignore_index=reservation_index
    )
    selected_room = next(
        (
            room for room in available_rooms
            if room["number"] == room_number
        ),
        None
    )
    if selected_room is None:
        raise ValueError(
            "La habitación seleccionada ya no está disponible "
            "o no admite esa cantidad de huéspedes."
        )

    nights = calculate_nights(check_in, check_out)
    if nights is None:
        raise ValueError("El Check Out debe ser posterior al Check In.")

    subtotal = calculate_subtotal(selected_room["price"], nights)
    igv = calculate_igv(subtotal)
    reservation = reservations[reservation_index]
    reservation.update({
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "guest_count": guest_count,
        "room_number": selected_room["number"],
        "room_type": selected_room["type"],
        "subtotal": subtotal,
        "igv": igv,
        "total": calculate_total(subtotal, igv)
    })

    save_reservations(reservations)
    return reservation


def get_available_rooms_for_reservation(
    reservation_index,
    guest_count,
    check_in,
    check_out
):
    return get_available_rooms(
        guest_count,
        check_in,
        check_out,
        ignore_index=reservation_index
    )