from reservations import *

def main():

    while True:

        print("\n===== HOSTEL MELIMER =====\n")

        print("1. Crear reserva")
        print("2. Ver mis reservas")
        print("3. Salir")


        option = input("\nSeleccione una opción: ")


        if option == "1":

            create_reservation()


        elif option == "2":

            show_customer_reservations()


        elif option == "3":

            print("\nGracias por utilizar el sistema.")

            break


        else:

            print("Opción inválida.")


if __name__ == "__main__":

    main()