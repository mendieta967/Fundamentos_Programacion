from storage.json_storage import (
    get_customer_by_dni,
    load_reservations
)


def frequent_customers():

    print("\n===== CLIENTES FRECUENTES =====\n")

    reservations = load_reservations()

    if not reservations:

        print("No hay reservas registradas.")

        return

    customers = {}

    for reservation in reservations:

        customer_dni = reservation["customer_dni"]

        if customer_dni in customers:

            customers[customer_dni] += 1

        else:

            customers[customer_dni] = 1

    ordered_customers = sorted(
        customers.items(),
        key=lambda customer: customer[1],
        reverse=True
    )

    found = False

    for customer_dni, reservation_count in ordered_customers:

        if reservation_count < 2:

            continue

        customer = get_customer_by_dni(
            customer_dni
        )

        print("-" * 40)

        print(f"Cliente: {customer['customer_name']}")
        print(f"DNI: {customer_dni}")
        print(f"Reservas: {reservation_count}")

        found = True

    if not found:

        print("No hay clientes frecuentes.")