from modules.helpers import show_reservation

from modules.validations import (
    custom_input,
    validate_dni
)

from storage.json_storage import (
    load_reservations
)


# ==========================================
# MOSTRAR RESERVAS DE UN CLIENTE
# ==========================================

def show_customer_reservations():

    customer_dni = custom_input(
        "Ingrese el DNI: "
    )

    if not validate_dni(customer_dni):

        print("DNI inválido.")

        return

    reservations = load_reservations()

    if not reservations:

        print("No hay reservas registradas.")

        return

    print("\n===== MIS RESERVAS =====\n")

    found_reservation = False

    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            found_reservation = True

            show_reservation(reservation)

    if not found_reservation:

        print("No se encontraron reservas para ese DNI.")