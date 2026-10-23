from .search import search_customer
from .history import show_customer_history
from .list import list_customers


def clients_menu():

    while True:

        print("\n===== GESTIÓN DE CLIENTES =====\n")

        print("1. Buscar cliente")
        print("2. Historial de reservas")
        print("3. Listar clientes")
        print("0. Volver")

        option = input("\nSeleccione una opción: ")

        if option == "1":

            search_customer()

        elif option == "2":

            show_customer_history()

        elif option == "3":
            
            list_customers()

        elif option == "0":

            break

        else:

            print("Opción inválida.")