from modules.helpers import show_customer
from modules.validations import custom_input, validate_dni, validate_phone
from storage.json_storage import get_customer_by_dni, get_customer_by_phone

def search_customer():

    while True:

        print("\n===== BUSCAR CLIENTE =====\n")

        print("1. Buscar por DNI")
        print("2. Buscar por teléfono")
        print("0. Volver")

        option = custom_input("\nSeleccione una opción: ")

        if option == "1":

            search_by_dni()

        elif option == "2":

            search_by_phone()

        elif option == "0":

            break

        else:

            print("Opción inválida.")

def search_by_dni():

    while True:

        customer_dni = custom_input(
            "Ingrese el DNI: "
        )

        if validate_dni(customer_dni):

            break

        print("DNI inválido.")

    customer = get_customer_by_dni(
        customer_dni
    )

    if customer:

        print("\n===== CLIENTE =====\n")

        show_customer(customer)

    else:

        print("\nCliente no encontrado.")

def search_by_phone():

    while True:

        customer_phone = custom_input(
            "Ingrese el teléfono: "
        )

        if validate_phone(customer_phone):

            break

        print("Teléfono inválido.")

    customer = get_customer_by_phone(
        customer_phone
    )

    if customer:

        print("\n===== CLIENTE =====\n")

        show_customer(customer)

    else:

        print("\nCliente no encontrado.")