from datetime import datetime

from .helpers import show_reservation

from modules.validations import custom_input

from storage.json_storage import load_reservations


def sort_reservations():

    while True:

        print("\n===== ORDENAR RESERVAS =====\n")

        print("1. Ordenar por Check-in")
        print("2. Ordenar por Check-out")
        print("3. Ordenar por Habitación")
        print("0. Volver")

        option = custom_input(
            "\nSeleccione una opción: "
        )

        if option == "1":

            sort_by_check_in()

            break

        elif option == "2":

            sort_by_check_out()

            break

        elif option == "3":

            sort_by_room()

            break

        elif option == "0":

            return

        else:

            print("Opción inválida.")

def sort_by_check_in():

    reservations = load_reservations()

    reservations.sort(

        key=lambda reservation:

        datetime.strptime(

            reservation["check_in"],

            "%d/%m/%Y"
        )

    )

    print("\n===== RESERVAS ORDENADAS POR CHECK-IN =====\n")

    show_sorted_reservations(reservations)

def sort_by_check_out():

    reservations = load_reservations()

    reservations.sort(

        key=lambda reservation:

        datetime.strptime(

            reservation["check_out"],

            "%d/%m/%Y"
        )

    )

    print("\n===== RESERVAS ORDENADAS POR CHECK-OUT =====\n")

    show_sorted_reservations(reservations)

def sort_by_room():

    reservations = load_reservations()

    reservations.sort(
        key=lambda reservation: reservation["room_number"]
    )

    print("\n===== RESERVAS ORDENADAS POR HABITACIÓN =====\n")

    show_sorted_reservations(reservations)

    
def show_sorted_reservations(reservations):

    if not reservations:

        print("No hay reservas registradas.")

        return

    for reservation in reservations:

        show_reservation(reservation)