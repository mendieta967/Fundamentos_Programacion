from storage.json_storage import load_reservations
from datetime import datetime


rooms = {

    # ===== SIMPLE ROOMS =====

    101: {
        "type": "Simple",
        "capacity": 1,
        "price": 50,
    },

    102: {
        "type": "Simple",
        "capacity": 1,
        "price": 50,
    },

    103: {
        "type": "Simple",
        "capacity": 1,
        "price": 50,
    },

    104: {
        "type": "Simple",
        "capacity": 1,
        "price": 50,
    },

    # ===== DOUBLE ROOMS =====

    201: {
        "type": "Double",
        "capacity": 2,
        "price": 80,
    },

    202: {
        "type": "Double",
        "capacity": 2,
        "price": 80,
    },

    203: {
        "type": "Double",
        "capacity": 2,
        "price": 80,
    },

    # ===== SUITES =====

    301: {
        "type": "Suite",
        "capacity": 4,
        "price": 120,
    },

    302: {
        "type": "Suite",
        "capacity": 4,
        "price": 120,
    },

    303: {
        "type": "Suite",
        "capacity": 4,
        "price": 120,
    }

}


# ==========================================
# MOSTRAR HABITACIONES DISPONIBLES
# ==========================================

def show_available_rooms(people_count, check_in, check_out):

    print("=" * 35)
    print("     HABITACIONES DISPONIBLES")
    print("=" * 35 + "\n")

    found_room = False

    for room_number, room_data in rooms.items():

        if (
            room_data["capacity"] >= people_count
            and
            is_room_available_for_dates(
                room_number,
                check_in,
                check_out
            )
        ):

            found_room = True

            print(
                f"{room_number} - "
                f"{room_data['type']} - "
                f"Capacidad: {room_data['capacity']} - "
                f"S/ {room_data['price']:.2f}"
            )

    if not found_room:

        print("No hay habitaciones disponibles.")


# ==========================================
# VERIFICAR SI EXISTE UNA HABITACIÓN
# ==========================================

def room_exists(room_number):

    return room_number in rooms


# ==========================================
# OBTENER INFORMACIÓN DE UNA HABITACIÓN
# ==========================================

def get_room(room_number):

    return rooms[room_number]


# ==========================================
# VALIDAR DISPONIBILIDAD
# ==========================================

def is_room_available_for_dates(
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

    for room_number, room in rooms.items():

        if room["capacity"] < guest_count:
            continue

        if not is_room_available_for_dates(
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
                "price": room["price"]
            }
        )

    return available_rooms