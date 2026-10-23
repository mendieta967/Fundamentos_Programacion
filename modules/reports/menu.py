from modules.reports.today import today_reservations
from modules.reports.frequent_customers import frequent_customers
from modules.reports.most_reserved_room import most_reserved_room
from modules.reports.most_profitable_room import most_profitable_room
from modules.reports.total_income import total_income


def reports_menu():

    while True:

        print("\n===== REPORTES =====\n")

        print("1. Reservas del día")
        print("2. Clientes frecuentes")
        print("3. Habitación más reservada")
        print("4. Habitación con mayor ingreso")
        print("5. Ingresos totales")
        print("0. Volver")

        option = input("\nSeleccione una opción: ")

        match option:

            case "1":

                today_reservations()

            case "2":

                frequent_customers()

            case "3":

                most_reserved_room()

            case "4":

                most_profitable_room()

            case "5":

                total_income()

            case "0":

                break

            case _:

                print("Opción inválida.")