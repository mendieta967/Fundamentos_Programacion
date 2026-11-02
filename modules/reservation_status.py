from storage.json_storage import load_reservations, save_reservations


def is_reservation_cancelled(reservation):
    status = str(reservation.get("status") or "").casefold()
    return status in {
        "cancelled",
        "cancelada"
    }


def active_reservations(reservations):
    return [
        reservation
        for reservation in reservations
        if not is_reservation_cancelled(reservation)
    ]


def cancel_reservation(reservation_index):
    reservations = load_reservations()
    if not 0 <= reservation_index < len(reservations):
        raise IndexError("La reserva ya no existe.")

    reservation = reservations[reservation_index]
    if is_reservation_cancelled(reservation):
        raise ValueError("Esta reserva ya está cancelada.")

    reservation["status"] = "cancelled"
    save_reservations(reservations)
    return reservation


def restore_reservation(reservation_index):
    reservations = load_reservations()
    if not 0 <= reservation_index < len(reservations):
        raise IndexError("La reserva ya no existe.")

    reservation = reservations[reservation_index]
    if not is_reservation_cancelled(reservation):
        raise ValueError("Esta reserva no está cancelada.")

    from modules.rooms import get_room, is_room_available_for_dates

    room = get_room(reservation["room_number"])
    if room["capacity"] < reservation["guest_count"]:
        raise ValueError(
            "La habitación ya no admite la cantidad de huéspedes "
            "de esta reserva."
        )

    if not is_room_available_for_dates(
        reservation["room_number"],
        reservation["check_in"],
        reservation["check_out"],
        ignore_index=reservation_index
    ):
        raise ValueError(
            "No se puede restaurar: la habitación está ocupada "
            "en esas fechas. Editá la reserva y elegí otras fechas "
            "o una habitación disponible."
        )

    reservation["status"] = "active"
    save_reservations(reservations)
    return reservation
