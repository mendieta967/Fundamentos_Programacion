from storage.json_storage import (
    load_reservations
)


# ==========================================
# FUNCIÓN RECURSIVA
# Caso base:
# Cuando el índice llega al final de la lista.
#
# Caso recursivo:
# Sumar el total de la reserva actual y
# llamar nuevamente a la función.
# ==========================================

def calculate_total_income(reservations, index=0):

    if index == len(reservations):

        return 0

    return (
        reservations[index]["total"]
        +
        calculate_total_income(
            reservations,
            index + 1
        )
    )


# ==========================================
# VERSIÓN ITERATIVA
# (Análisis comparativo)
# ==========================================

def calculate_total_income_iterative(reservations):

    total = 0

    for reservation in reservations:

        total += reservation["total"]

    return total


# ==========================================
# REPORTE
# ==========================================

def total_income():

    print("\n===== INGRESOS TOTALES =====\n")

    reservations = load_reservations()

    if not reservations:

        print("No hay reservas registradas.")

        return

    total = calculate_total_income(
        reservations
    )

    print(f"Cantidad de reservas: {len(reservations)}")
    print(f"Ingresos totales: S/ {total:.2f}")