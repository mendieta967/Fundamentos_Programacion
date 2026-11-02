from modules.helpers import show_reservation

from .update import select_reservation
from modules.validations import custom_input

from modules.reservation_status import cancel_reservation


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
            "\n¿Está seguro de cancelar esta reserva? (s/n): "
        ).lower()

        if confirm in ["s", "n"]:

            break

        print("Opción inválida.")

    if confirm == "n":

        print("\nCancelación anulada.")

        return

    cancel_reservation(reservation_index)
    print("\nReserva cancelada. Se conservó en el historial.")