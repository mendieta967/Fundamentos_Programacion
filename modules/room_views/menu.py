from modules.room_views.list import list_rooms
from modules.room_views.search import search_room


def rooms_menu():

    while True:

        print("\n===== GESTIÓN DE HABITACIONES =====\n")

        print("1. Listar habitaciones")
        print("2. Buscar habitación")
        print("0. Volver")

        option = input("\nSeleccione una opción: ")

        match option:

            case "1":

                list_rooms()

            case "2":

                search_room()

            case "0":

                break

            case _:

                print("Opción inválida.")