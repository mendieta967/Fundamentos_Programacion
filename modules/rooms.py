import json
import math
from pathlib import Path

from storage.json_storage import load_reservations
from modules.reservation_status import is_reservation_cancelled
from datetime import datetime


ROOMS_FILE = Path(__file__).resolve().parents[1] / "data" / "rooms.json"


def get_rooms():
    try:
        with ROOMS_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"No se encontró el inventario de habitaciones: {ROOMS_FILE}"
        ) from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo de habitaciones no contiene JSON válido: "
            f"{ROOMS_FILE} (línea {error.lineno}, columna {error.colno})."
        ) from error

    if not isinstance(records, list) or not records:
        raise ValueError("El inventario de habitaciones debe ser una lista.")

    rooms_by_number = {}
    for room in records:
        if not isinstance(room, dict):
            raise ValueError("Cada habitación debe ser un objeto JSON.")

        number = room.get("number")
        room_type = room.get("type")
        capacity = room.get("capacity")
        price = room.get("price")
        maintenance = room.get("maintenance", False)

        if isinstance(number, bool) or not isinstance(number, int):
            raise ValueError("Cada habitación debe tener un número entero.")
        if number in rooms_by_number:
            raise ValueError(f"La habitación {number} está duplicada.")
        if not isinstance(room_type, str) or not room_type.strip():
            raise ValueError(f"El tipo de la habitación {number} es inválido.")
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValueError(f"La capacidad de la habitación {number} es inválida.")
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or (
                isinstance(price, float)
                and not math.isfinite(price)
            )
            or price < 0
        ):
            raise ValueError(f"El precio de la habitación {number} es inválido.")
        if not isinstance(maintenance, bool):
            raise ValueError(
                f"El estado de mantenimiento de la habitación {number} "
                "debe ser verdadero o falso."
            )

        rooms_by_number[number] = {
            "type": room_type.strip(),
            "capacity": capacity,
            "price": price,
            "maintenance": maintenance
        }

    return rooms_by_number


def save_rooms(rooms_by_number):
    records = [
        {
            "number": number,
            "type": room["type"],
            "capacity": room["capacity"],
            "price": room["price"],
            "maintenance": room.get("maintenance", False)
        }
        for number, room in sorted(rooms_by_number.items())
    ]

    with ROOMS_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)


def set_room_price(room_number, price):
    if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or (
            isinstance(price, float)
            and not math.isfinite(price)
        )
        or price < 0
    ):
        raise ValueError("El precio debe ser un número mayor o igual a cero.")

    all_rooms = get_rooms()
    if room_number not in all_rooms:
        raise KeyError(f"La habitación {room_number} no existe.")

    all_rooms[room_number]["price"] = price
    save_rooms(all_rooms)
    return all_rooms[room_number]


def set_room_maintenance(room_number, in_maintenance):
    if not isinstance(in_maintenance, bool):
        raise ValueError("El estado de mantenimiento debe ser verdadero o falso.")

    all_rooms = get_rooms()
    if room_number not in all_rooms:
        raise KeyError(f"La habitación {room_number} no existe.")

    all_rooms[room_number]["maintenance"] = in_maintenance
    save_rooms(all_rooms)
    return all_rooms[room_number]


# ==========================================
# MOSTRAR HABITACIONES DISPONIBLES
# ==========================================

def show_available_rooms(people_count, check_in, check_out):

    print("=" * 35)
    print("     HABITACIONES DISPONIBLES")
    print("=" * 35 + "\n")

    available_rooms = get_available_rooms(
        people_count,
        check_in,
        check_out
    )
    for room in available_rooms:
        print(
            f"{room['number']} - "
            f"{room['type']} - "
            f"Capacidad: {room['capacity']} - "
            f"S/ {room['price']:.2f}"
        )

    if not available_rooms:

        print("No hay habitaciones disponibles.")


# ==========================================
# VERIFICAR SI EXISTE UNA HABITACIÓN
# ==========================================

def room_exists(room_number):

    return room_number in get_rooms()


# ==========================================
# OBTENER INFORMACIÓN DE UNA HABITACIÓN
# ==========================================

def get_room(room_number):

    return get_rooms()[room_number]


# ==========================================
# VALIDAR DISPONIBILIDAD
# ==========================================

def is_room_available_for_dates(
    room_number,
    check_in,
    check_out,
    ignore_index=None
):

    room = get_room(room_number)
    if room["maintenance"]:
        return False

    return _is_room_available_for_dates(
        room_number,
        check_in,
        check_out,
        ignore_index
    )


def _is_room_available_for_dates(
    room_number,
    check_in,
    check_out,
    ignore_index=None
):
    reservations = load_reservations()

    new_check_in = datetime.strptime(
        check_in,
        "%d/%m/%Y"
    )

    new_check_out = datetime.strptime(
        check_out,
        "%d/%m/%Y"
    )

    for index, reservation in enumerate(reservations):

        # Ignorar la reserva que se está modificando
        if index == ignore_index:

            continue

        if is_reservation_cancelled(reservation):
            continue

        if reservation["room_number"] == room_number:

            existing_check_in = datetime.strptime(
                reservation["check_in"],
                "%d/%m/%Y"
            )

            existing_check_out = datetime.strptime(
                reservation["check_out"],
                "%d/%m/%Y"
            )

            if (
                new_check_in < existing_check_out
                and
                new_check_out > existing_check_in
            ):

                return False

    return True


# ==========================================
# OBTENER RESERVA ACTUAL DE UNA HABITACIÓN
# ==========================================

def get_room_current_reservation(room_number):

    reservations = load_reservations()

    today = datetime.today().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    for reservation in reservations:

        if is_reservation_cancelled(reservation):
            continue

        if reservation["room_number"] != room_number:

            continue

        check_in = datetime.strptime(
            reservation["check_in"],
            "%d/%m/%Y"
        )

        check_out = datetime.strptime(
            reservation["check_out"],
            "%d/%m/%Y"
        )

        if check_in <= today <= check_out:

            return reservation

    return None


# ==========================================
# SELECCIONAR HABITACIÓN
# ==========================================

def select_room(
    guest_count,
    check_in,
    check_out,
    ignore_index=None
):

    show_available_rooms(
        guest_count,
        check_in,
        check_out
    )

    while True:

        room_number = input(
            "Seleccione una habitación: "
        )

        if not room_number.isdigit():

            print("Debe ingresar un número de habitación.")
            continue

        room_number = int(room_number)

        if not room_exists(room_number):

            print("La habitación no existe.")
            continue

        room = get_room(room_number)

        if room["capacity"] < guest_count:

            print(
                "La habitación no soporta esa cantidad de huéspedes."
            )

            continue

        if not is_room_available_for_dates(
            room_number,
            check_in,
            check_out,
            ignore_index
        ):

            print(
                "La habitación ya está reservada para esas fechas."
            )

            continue

        return room_number, room

# ==========================================
# OBTENER HABITACIONES DISPONIBLES
# ==========================================

def get_available_rooms(
    guest_count,
    check_in,
    check_out,
    ignore_index=None
):

    available_rooms = []

    for room_number, room in get_rooms().items():

        if room["maintenance"]:
            continue
        if room["capacity"] < guest_count:
            continue

        if not _is_room_available_for_dates(
            room_number,
            check_in,
            check_out,
            ignore_index
        ):
            continue

        available_rooms.append(
            {
                "number": room_number,
                "type": room["type"],
                "capacity": room["capacity"],
                "price": room["price"],
                "maintenance": room["maintenance"]
            }
        )

    return available_rooms