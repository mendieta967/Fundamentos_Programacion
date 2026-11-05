from collections import Counter, defaultdict
from datetime import date, datetime

from modules.reservation_status import active_reservations
from modules.rooms import get_rooms
from storage.json_storage import load_customers, load_reservations


DATE_FORMAT = "%d/%m/%Y"


def _as_date(value):
    return datetime.strptime(value, DATE_FORMAT).date()


def _load_report_records():
    reservations = active_reservations(load_reservations())
    customers = {
        customer["customer_dni"]: customer
        for customer in load_customers()
    }
    return reservations, customers


def _currency(amount):
    return f"S/ {amount:,.2f}".replace(",", " ")


def _today_report(reservations, customers, today):
    arrivals = [
        reservation
        for reservation in reservations
        if _as_date(reservation["check_in"]) == today
    ]
    arrivals.sort(
        key=lambda reservation: (
            reservation["check_in"],
            reservation["customer_dni"]
        )
    )

    rows = [
        (
            customers.get(reservation["customer_dni"], {}).get(
                "customer_name",
                "Cliente sin registro"
            ),
            reservation["customer_dni"],
            str(reservation["room_number"]),
            reservation["check_in"],
            reservation["check_out"]
        )
        for reservation in arrivals
    ]
    guest_count = sum(reservation.get("guest_count", 0) for reservation in arrivals)

    return {
        "columns": ("Cliente", "DNI", "Habitación", "Check-in", "Check-out"),
        "rows": rows,
        "metrics": (
            ("LLEGADAS PROGRAMADAS", str(len(arrivals)), "Reservas con ingreso hoy"),
            ("HUÉSPEDES", str(guest_count), "Personas que llegan hoy")
        ),
        "note": "Se excluyen las reservas canceladas."
    }


def _frequent_customers_report(reservations, customers):
    counts = Counter(
        reservation["customer_dni"]
        for reservation in reservations
    )
    ordered = sorted(
        counts.items(),
        key=lambda item: (
            -item[1],
            customers.get(item[0], {}).get("customer_name", "").casefold()
        )
    )
    rows = [
        (
            customers.get(dni, {}).get("customer_name", "Cliente sin registro"),
            dni,
            str(count)
        )
        for dni, count in ordered
    ]

    return {
        "columns": ("Cliente", "DNI", "Reservas"),
        "rows": rows,
        "metrics": (
            ("CLIENTES", str(len(counts)), "Con al menos una reserva"),
            (
                "MÁS FRECUENTE",
                rows[0][0] if rows else "—",
                f"{rows[0][2]} reservas" if rows else "Sin reservas registradas"
            )
        ),
        "note": "Historial completo, ordenado por cantidad de reservas; se excluyen las canceladas."
    }


def _room_demand_report(reservations, rooms):
    counts = Counter(
        reservation["room_number"]
        for reservation in reservations
    )
    room_numbers = set(rooms).union(counts)
    ordered_rooms = sorted(
        room_numbers,
        key=lambda number: (-counts[number], number)
    )
    rows = [
        (
            str(number),
            rooms.get(number, {}).get("type", "Sin inventario"),
            str(counts[number])
        )
        for number in ordered_rooms
    ]
    top_room = ordered_rooms[0] if ordered_rooms and counts[ordered_rooms[0]] else None
    top_room_type = (
        rooms.get(top_room, {}).get("type", "Sin inventario")
        if top_room is not None
        else None
    )

    return {
        "columns": ("Habitación", "Tipo", "Reservas"),
        "rows": rows,
        "metrics": (
            (
                "MAYOR DEMANDA",
                f"{top_room} - {top_room_type}" if top_room is not None else "—",
                f"{counts[top_room]} reservas" if top_room is not None else "Sin reservas registradas"
            ),
            ("HABITACIONES", str(len(rooms)), "En el inventario")
        ),
        "note": "Historial completo: cada reserva cuenta una vez para su habitación; se excluyen las canceladas."
    }


def _room_income_report(reservations, rooms):
    totals = defaultdict(float)
    for reservation in reservations:
        totals[reservation["room_number"]] += float(reservation["total"])

    room_numbers = set(rooms).union(totals)
    ordered_rooms = sorted(
        room_numbers,
        key=lambda number: (-totals[number], number)
    )
    rows = [
        (
            str(number),
            rooms.get(number, {}).get("type", "Sin inventario"),
            _currency(totals[number])
        )
        for number in ordered_rooms
    ]
    top_room = ordered_rooms[0] if ordered_rooms and totals[ordered_rooms[0]] else None
    top_room_type = (
        rooms.get(top_room, {}).get("type", "Sin inventario")
        if top_room is not None
        else None
    )

    return {
        "columns": ("Habitación", "Tipo", "Total facturado"),
        "rows": rows,
        "metrics": (
            (
                "MAYOR FACTURACIÓN",
                f"{top_room} - {top_room_type}" if top_room is not None else "—",
                _currency(totals[top_room]) if top_room is not None else "Sin reservas registradas"
            ),
            ("HABITACIONES", str(len(rooms)), "En el inventario")
        ),
        "note": "Historial completo: se suma el total de reservas no canceladas asociadas a cada habitación."
    }


def _total_income_report(reservations, customers):
    total = sum(float(reservation["total"]) for reservation in reservations)
    count = len(reservations)
    average = total / count if count else 0

    return {
        "columns": ("Cliente", "DNI", "Habitación", "Check-in", "Total facturado"),
        "rows": [
            (
                customer_name,
                reservation["customer_dni"],
                str(reservation["room_number"]),
                reservation["check_in"],
                _currency(float(reservation["total"]))
            )
            for reservation, customer_name in sorted(
                (
                    (
                        reservation,
                        customers.get(reservation["customer_dni"], {}).get(
                            "customer_name",
                            "Cliente sin registro"
                        )
                    )
                    for reservation in reservations
                ),
                key=lambda item: _as_date(item[0]["check_in"]),
                reverse=True
            )
        ],
        "metrics": (
            ("TOTAL FACTURADO", _currency(total), "Reservas no canceladas"),
            ("TOTAL RESERVAS", str(count), "Reservas consideradas"),
            ("PROMEDIO POR RESERVA", _currency(average), "Total facturado ÷ reservas")
        ),
        "note": "Historial completo de reservas no canceladas. Es total facturado, no dinero efectivamente cobrado."
    }


def _occupancy_report(reservations, rooms, today):
    operational_rooms = {
        number: room
        for number, room in rooms.items()
        if not room["maintenance"]
    }
    occupied_numbers = {
        reservation["room_number"]
        for reservation in reservations
        if (
            _as_date(reservation["check_in"]) <= today
            and _as_date(reservation["check_out"]) > today
            and reservation["room_number"] in operational_rooms
        )
    }
    available = len(operational_rooms) - len(occupied_numbers)
    occupancy = (
        len(occupied_numbers) / len(operational_rooms) * 100
        if operational_rooms
        else 0
    )

    rows = []
    for number, room in sorted(rooms.items()):
        if room["maintenance"]:
            status = "Mantenimiento"
        elif number in occupied_numbers:
            status = "Ocupada"
        else:
            status = "Disponible"
        rows.append((str(number), room["type"], status))

    return {
        "columns": ("Habitación", "Tipo", "Estado de hoy"),
        "rows": rows,
        "metrics": (
            ("OCUPACIÓN", f"{occupancy:.0f} %", "Sobre habitaciones operativas"),
            ("OCUPADAS", str(len(occupied_numbers)), "Con estadía que incluye hoy"),
            ("DISPONIBLES", str(available), "Operativas y libres hoy"),
            ("MANTENIMIENTO", str(len(rooms) - len(operational_rooms)), "Fuera del cálculo")
        ),
        "note": "Una habitación está ocupada si check-in ≤ hoy < check-out; se excluyen cancelaciones."
    }


def get_report_data(report_key, today=None):
    valid_reports = {
        "today",
        "frequent_customers",
        "most_reserved_room",
        "room_income",
        "total_income",
        "occupancy"
    }
    if report_key not in valid_reports:
        raise ValueError(f"El reporte «{report_key}» no está definido.")

    today = today or date.today()
    reservations, customers = _load_report_records()

    if report_key == "today":
        return _today_report(reservations, customers, today)
    if report_key == "frequent_customers":
        return _frequent_customers_report(reservations, customers)
    if report_key == "most_reserved_room":
        return _room_demand_report(reservations, get_rooms())
    if report_key == "room_income":
        return _room_income_report(reservations, get_rooms())
    if report_key == "total_income":
        return _total_income_report(reservations, customers)
    if report_key == "occupancy":
        return _occupancy_report(reservations, get_rooms(), today)
