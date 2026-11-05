from modules.payments import calculate_igv, calculate_subtotal, calculate_total
from modules.reservation_status import is_reservation_cancelled
from modules.rooms import get_available_rooms
from modules.validations import (
    calculate_nights,
    validate_date,
    validate_future_date,
    validate_guest_count
)
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

    reservation = reservations[reservation_index]
    if is_reservation_cancelled(reservation):
        raise ValueError(
            "Una reserva cancelada no se puede editar. "
            "Usá «Reprogramar y reactivar» para crear una nueva reserva."
        )

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


def rebook_cancelled_reservation(
    reservation_index,
    check_in,
    check_out,
    guest_count,
    room_number
):
    reservations = load_reservations()
    if not 0 <= reservation_index < len(reservations):
        raise IndexError("La reserva ya no existe.")

    cancelled_reservation = reservations[reservation_index]
    if not is_reservation_cancelled(cancelled_reservation):
        raise ValueError("Esta reserva ya no está cancelada.")

    if not validate_date(check_in) or not validate_future_date(check_in):
        raise ValueError("El Check In debe ser hoy o una fecha futura válida.")
    if not validate_date(check_out):
        raise ValueError("Ingresá un Check Out válido.")
    if not validate_guest_count(str(guest_count)):
        raise ValueError("La cantidad de huéspedes debe ser entre 1 y 4.")

    nights = calculate_nights(check_in, check_out)
    if nights is None:
        raise ValueError("El Check Out debe ser posterior al Check In.")

    available_rooms = get_available_rooms(
        guest_count,
        check_in,
        check_out
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

    subtotal = calculate_subtotal(selected_room["price"], nights)
    igv = calculate_igv(subtotal)
    new_reservation = dict(cancelled_reservation)
    new_reservation.update({
        "status": "active",
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

    reservations.append(new_reservation)
    save_reservations(reservations)
    return new_reservation


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