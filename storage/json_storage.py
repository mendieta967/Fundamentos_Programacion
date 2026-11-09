import json
from pathlib import Path


# ==========================================
# RUTAS DE LOS ARCHIVOS
# ==========================================

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RESERVATIONS_FILE = DATA_DIR / "reservations.json"
CUSTOMERS_FILE = DATA_DIR / "customers.json"


# ==========================================
# RESERVAS
# ==========================================

def load_reservations():
    try:
        with RESERVATIONS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            "El archivo de reservas contiene JSON inválido "
            f"(línea {error.lineno}, columna {error.colno}): "
            f"{RESERVATIONS_FILE}"
        ) from error


def save_reservations(reservations):

    with RESERVATIONS_FILE.open("w", encoding="utf-8") as file:

        json.dump(
            reservations,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# CLIENTES
# ==========================================

def load_customers():
    try:
        with CUSTOMERS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            "El archivo de clientes contiene JSON inválido "
            f"(línea {error.lineno}, columna {error.colno}): "
            f"{CUSTOMERS_FILE}"
        ) from error


def save_customers(customers):

    with CUSTOMERS_FILE.open("w", encoding="utf-8") as file:

        json.dump(
            customers,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# VERIFICAR SI EXISTE UN CLIENTE
# ==========================================

def customer_exists(customer_dni):

    customers = load_customers()

    for customer in customers:

        if customer["customer_dni"] == customer_dni:

            return True

    return False


# ==========================================
# OBTENER TODOS LOS CLIENTES
# ==========================================

def get_all_customers():

    return load_customers()


# ==========================================
# BUSCAR CLIENTE POR DNI
# ==========================================

def get_customer_by_dni(customer_dni):

    customers = load_customers()

    for customer in customers:

        if customer["customer_dni"] == customer_dni:

            return customer

    return None


# ==========================================
# BUSCAR CLIENTE POR TELÉFONO
# ==========================================

def get_customer_by_phone(customer_phone):

    customers = load_customers()

    for customer in customers:

        if customer["customer_phone"] == customer_phone:

            return customer

    return None

# ==========================================
# VERIFICAR SI UN CLIENTE TIENE RESERVAS
# ==========================================

def customer_has_reservations(customer_dni):

    reservations = load_reservations()

    for reservation in reservations:

        if reservation["customer_dni"] == customer_dni:

            return True

    return False


# ==========================================
# ELIMINAR CLIENTE
# ==========================================

def delete_customer(customer_dni):

    customers = load_customers()

    updated_customers = []

    for customer in customers:

        if customer["customer_dni"] != customer_dni:

            updated_customers.append(customer)

    save_customers(updated_customers)