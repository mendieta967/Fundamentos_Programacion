from modules.helpers import show_customer

from storage.json_storage import (
    get_all_customers
)

def list_customers():

    customers = get_all_customers()

    print("\n===== LISTA DE CLIENTES =====\n")

    if not customers:

        print("No hay clientes registrados.")

        return

    for customer in customers:

        show_customer(customer)