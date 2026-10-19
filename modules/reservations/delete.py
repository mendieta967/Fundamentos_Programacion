from .update import select_reservation
from storage.json_storage import save_reservations
from modules.validations import custom_input


def delete_reservation():

    print("\n===== ELIMINAR RESERVA =====\n")

    reservations, reservation_index, reservation = select_reservation()

    if reservations is None:

        return

    print("\n===== RESERVA SELECCIONADA =====\n")

    print(f"Cliente: {reservation['customer_name']}")
    print(f"DNI: {reservation['customer_dni']}")
    print(f"Habitación: {reservation['room_number']}")
    print(f"Check-in: {reservation['check_in']}")
    print(f"Check-out: {reservation['check_out']}")
    print(f"Total: ${reservation['total']}")

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

    reservations.pop(reservation_index)

    save_reservations(reservations)

    print("\nReserva eliminada correctamente.")