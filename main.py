from modules.reservations import reservations_menu

def main():

    while True:

        print("\n===== HOSTEL MELIMER =====\n")

        print("1. Gestión de Reservas")
        print("2. Gestión de Clientes")
        print("3. Gestión de Habitaciones")
        print("4. Reportes")
        print("0. Salir")


        option = input("\nSeleccione una opción: ")


        if option == "1":

            reservations_menu()

        elif option == "0":

            print("\nGracias por utilizar el sistema.")

            break


        else:

            print("Opción inválida.")


if __name__ == "__main__":

    main()