from datetime import datetime

from modules.helpers import show_reservation

from modules.rooms import room_exists
from modules.validations import (
    custom_input,
    validate_date,
    validate_dni
)

from storage.json_storage import (
    load_reservations
)


# ==========================================
# MENÚ DE BÚSQUEDA
# ==========================================

def search_reservation():

    while True:

        print("\n===== BUSCAR RESERVA =====\n")

        print("1. Buscar por DNI")
        print("2. Buscar por Habitación")
        print("3. Buscar por Fecha")
        print("0. Volver")

        option = custom_input(
            "\nSeleccione una opción: "
        )

        if option == "1":

            search_by_dni()
            return

        elif option == "2":

            search_by_room()
            return

        elif option == "3":

            search_by_date()
            return

        elif option == "0":

            return

        else:

            print("Opción inválida.")


# ==========================================
# BUSCAR POR DNI
# ==========================================

def search_by_dni():

    customer_dni = custom_input(
        "Ingrese el DNI: "
    )

    if not validate_dni(customer_dni):

        print("DNI inválido.")
        return

    reservations = load_reservations()

    found = False

    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            show_reservation(reservation)

            found = True

    if not found:

        print("\nNo se encontraron reservas.")


# ==========================================
# BUSCAR POR HABITACIÓN
# ==========================================

def search_by_room():

    room_number = custom_input(
        "Ingrese el número de habitación: "
    )

    if not room_number.isdigit():

        print("Número inválido.")
        return

    room_number = int(room_number)

    if not room_exists(room_number):

        print("La habitación no existe.")
        return

    reservations = load_reservations()

    found = False

    for reservation in reservations:

        if reservation["room_number"] == room_number:

            show_reservation(reservation)

            found = True

    if not found:

        print("\nNo se encontraron reservas para esa habitación.")


# ==========================================
# BUSCAR POR FECHA
# ==========================================

def search_by_date():

    search_date = custom_input(
        "Ingrese la fecha (dd/mm/yyyy): "
    )

    if not validate_date(search_date):

        print("Fecha inválida.")
        return

    search_date = datetime.strptime(
        search_date,
        "%d/%m/%Y"
    )

    reservations = load_reservations()

    found = False

    for reservation in reservations:

        check_in = datetime.strptime(
            reservation["check_in"],
            "%d/%m/%Y"
        )

        check_out = datetime.strptime(
            reservation["check_out"],
            "%d/%m/%Y"
        )

        if check_in <= search_date <= check_out:

            show_reservation(reservation)

            found = True

    if not found:

        print("\nNo se encontraron reservas para esa fecha.")