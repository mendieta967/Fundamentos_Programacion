from modules.validations import (
    custom_input,
    validate_dni,
)

from .helpers import show_reservation

from storage.json_storage import load_reservations


def show_customer_reservations():

    customer_dni = custom_input(
        "Ingrese su DNI: "
    )

    if not validate_dni(customer_dni):

        print("DNI inválido.")

        return

    reservations = load_reservations()

    found_reservation = False

    print("\n===== MIS RESERVAS =====\n")

    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            found_reservation = True

            show_reservation(reservation)

    if not found_reservation:

        print("No se encontraron reservas para ese DNI.")