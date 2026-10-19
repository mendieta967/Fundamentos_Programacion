from .create import create_reservation
from .read import show_customer_reservations
from .update import modify_reservation
from .delete import delete_reservation
from .search import search_reservation
from .sort import sort_reservations

from modules.validations import custom_input


def reservations_menu():

    while True:

        print("\n===== GESTIÓN DE RESERVAS =====\n")

        print("1. Registrar reserva")
        print("2. Ver reservas")
        print("3. Modificar reserva")
        print("4. Eliminar reserva")
        print("5. Buscar reserva")
        print("6. Ordenar reservas")
        print("0. Volver")

        option = custom_input(
            "\nSeleccione una opción: "
        )

        if option == "1":

            create_reservation()

        elif option == "2":

            show_customer_reservations()

        elif option == "3":

            modify_reservation()

        elif option == "4":

            delete_reservation()

        elif option == "5":

            search_reservation()

        elif option == "6":

            sort_reservations()

        elif option == "0":

            break

        else:

            print("Opción inválida.")