from modules.helpers import show_customer, show_reservation
from modules.validations import custom_input, validate_dni
from storage.json_storage import get_customer_by_dni, load_reservations


def show_customer_history():

    print("\n===== HISTORIAL DE RESERVAS =====\n")

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

    if customer is None:

        print("\nCliente no encontrado.")

        return

    print("\n===== CLIENTE =====\n")

    show_customer(customer)

    reservations = load_reservations()

    found_reservation = False

    print("\n===== RESERVAS =====\n")

    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            found_reservation = True

            show_reservation(reservation)

    if not found_reservation:

        print("Este cliente no posee reservas registradas.")