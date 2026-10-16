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
# Función para mostrar habitaciones disponibles según la cantidad de personas
# La cantidad de personas se pasa como parametro a la función, y se muestra solo las habitaciones que tienen capacidad suficiente y están disponibles.
def show_available_rooms(people_count,check_in,check_out):
    print("=" * 35)
    print("     HABITACIONES DISPONIBLES")
    print("=" * 35 + "\n")

# Variable para controlar si se encontraron habitaciones disponibles
    found_room = False

# Iterar sobre las habitaciones y mostrar solo las que cumplen con los criterios
# room_number es el número de la habitación, y room_data es un diccionario con los detalles de la habitación (tipo, capacidad, precio, disponibilidad).
# rooms.items() devuelve una lista de tuplas, donde cada tupla contiene el número de la habitación y su información asociada. Esto permite iterar sobre todas las habitaciones y acceder a sus detalles para verificar si cumplen con los criterios de capacidad y disponibilidad.
    for room_number, room_data in rooms.items():

# Si la capacidad de la habitación es mayor o igual a la cantidad de personas y la habitación está disponible
        if room_data["capacity"] >= people_count and is_room_available_for_dates(room_number,check_in,check_out):

# Se marca que se encontró al menos una habitación disponible para esa cantidad de personas
            found_room = True

# Se muestra la información de la habitación
            print(
                f"{room_number} - "
                f'{room_data["type"]} - '
                f'Capacity: {room_data["capacity"]} - '
                f'${room_data["price"]}'
            )

# Si no se encontraron habitaciones disponibles para esa cantidad de personas, se muestra un mensaje indicando que no hay habitaciones disponibles.
    if not found_room:
        print("No hay habitaciones disponible")

# Función para verificar si una habitación existe dado su número
def room_exists(room_number):
    return room_number in rooms

# Función para obtener la información de una habitación dado su número
def get_room(room_number):
    return rooms[room_number]

def is_room_available_for_dates(room_number, check_in, check_out):
    reservations = load_reservations()
    new_check_in = datetime.strptime(check_in, "%d/%m/%Y")

    new_check_out = datetime.strptime(check_out, "%d/%m/%Y")

    for reservation in reservations:
        if reservation["room_number"] == room_number:
            existing_check_in = datetime.strptime(reservation["check_in"],"%d/%m/%Y")
            existing_check_out = datetime.strptime(reservation["check_out"],"%d/%m/%Y")
            if new_check_in < existing_check_out and new_check_out > existing_check_in:
                return False
    return True