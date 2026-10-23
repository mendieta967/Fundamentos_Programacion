from modules.reservations.menu import reservations_menu
from modules.validations import custom_input
from modules.clients.menu import clients_menu


def main():

    while True:

        print("\n===== HOSTEL MELIMER =====\n")

        print("1. Gestión de Reservas")
        print("2. Gestión de Clientes")
        print("3. Gestión de Habitaciones")
        print("4. Reportes")
        print("0. Salir")

        option = custom_input(
            "\nSeleccione una opción: "
        )

        if option == "1":

            reservations_menu() 

        elif option == "2":

            clients_menu()

        elif option == "3":

            print("Módulo en desarrollo.")

        elif option == "4":

            print("Módulo en desarrollo.")

        elif option == "0":

            print("\nGracias por utilizar el sistema.")

            break

        else:

            print("Opción inválida.")


if __name__ == "__main__":

    main()