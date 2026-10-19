from modules.validations import custom_input, validate_date, validate_dni
from storage.json_storage import load_reservations
from datetime import datetime

def search_reservation():

    while True:

        print("\n===== BUSCAR RESERVA =====\n")

        print("1. Buscar por DNI")
        print("2. Buscar por Habitación")
        print("3. Buscar por Fecha")
        print("0. Volver")

        option = custom_input("\nSeleccione una opción: ")

        if option == "1":

            search_by_dni()
            break

        elif option == "2":

            search_by_room()
            break

        elif option == "3":

            search_by_date()
            break

        elif option == "0":

            return

        else:

            print("Opción inválida.")

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

    print(f"Total: S/ {reservation['total']}")

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

def search_by_room():

    room_number = custom_input(
        "Ingrese el número de habitación: "
    )

    if not room_number.isdigit():

        print("Número inválido.")
        return

    room_number = int(room_number)

    reservations = load_reservations()

    found = False

    for reservation in reservations:

        if reservation["room_number"] == room_number:

            show_reservation(reservation)

            found = True

    if not found:

        print("\nNo se encontraron reservas.")

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

        if check_in <= search_date < check_out:

            show_reservation(reservation)

            found = True

    if not found:

        print("\nNo se encontraron reservas para esa fecha.")