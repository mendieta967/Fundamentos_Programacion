from modules.helpers import show_reservation

from .update import select_reservation
from modules.validations import custom_input

from storage.json_storage import (
    customer_has_reservations,
    delete_customer,
    save_reservations
)


# ==========================================
# ELIMINAR RESERVA
# ==========================================

def delete_reservation():

    print("\n===== ELIMINAR RESERVA =====\n")

    reservations, reservation_index, reservation = (
        select_reservation()
    )

    if reservations is None:

        return

    print("\n===== RESERVA SELECCIONADA =====")

    show_reservation(reservation)

    while True:

        confirm = custom_input(
            "\n¿Está seguro de eliminar esta reserva? (s/n): "
        ).lower()

        if confirm in ["s", "n"]:

            break

        print("Opción inválida.")

    if confirm == "n":

        print("\nEliminación cancelada.")

        return

    customer_dni = reservation["customer_dni"]

    reservations.pop(reservation_index)

    save_reservations(reservations)

    print("\nReserva eliminada correctamente.")

    # ==========================================
    # ELIMINAR CLIENTE SI YA NO TIENE RESERVAS
    # ==========================================

    if not customer_has_reservations(customer_dni):

        while True:

            option = custom_input(
                "\nEl cliente ya no tiene reservas.\n"
                "¿Desea eliminar también al cliente? (s/n): "
            ).lower()

            if option in ["s", "n"]:

                break

            print("Opción inválida.")

        if option == "s":

            delete_customer(customer_dni)

            print("Cliente eliminado correctamente.")