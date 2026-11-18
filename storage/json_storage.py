import json
import os
import tempfile
from pathlib import Path
from threading import RLock


DATA_LOCK = RLock()


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
            reservations = json.load(file)
            if not isinstance(reservations, list):
                raise ValueError("El archivo de reservas debe contener una lista.")
            return reservations
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            "El archivo de reservas contiene JSON inválido "
            f"(línea {error.lineno}, columna {error.colno}): "
            f"{RESERVATIONS_FILE}"
        ) from error


def save_json_atomic(file_path, records):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp",
            delete=False
        ) as file:
            temporary_path = Path(file.name)
            json.dump(records, file, indent=4, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, file_path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise


def save_reservations(reservations):
    if not isinstance(reservations, list):
        raise ValueError("Las reservas deben almacenarse como una lista.")

    required_fields = {
        "customer_dni",
        "check_in",
        "check_out",
        "room_number",
        "total"
    }
    for index, reservation in enumerate(reservations):
        if not isinstance(reservation, dict):
            raise ValueError(f"La reserva {index} debe ser un objeto JSON.")
        missing = required_fields.difference(reservation)
        if missing:
            raise ValueError(
                f"La reserva {index} no tiene los campos requeridos: "
                f"{', '.join(sorted(missing))}."
            )

    save_json_atomic(RESERVATIONS_FILE, reservations)


# ==========================================
# CLIENTES
# ==========================================

def load_customers():
    try:
        with CUSTOMERS_FILE.open("r", encoding="utf-8") as file:
            customers = json.load(file)
            if not isinstance(customers, list):
                raise ValueError("El archivo de clientes debe contener una lista.")
            return customers
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            "El archivo de clientes contiene JSON inválido "
            f"(línea {error.lineno}, columna {error.colno}): "
            f"{CUSTOMERS_FILE}"
        ) from error


def save_customers(customers):
    if not isinstance(customers, list):
        raise ValueError("Los clientes deben almacenarse como una lista.")

    required_fields = {"customer_name", "customer_dni", "customer_phone"}
    for index, customer in enumerate(customers):
        if not isinstance(customer, dict):
            raise ValueError(f"El cliente {index} debe ser un objeto JSON.")
        missing = required_fields.difference(customer)
        if missing:
            raise ValueError(
                f"El cliente {index} no tiene los campos requeridos: "
                f"{', '.join(sorted(missing))}."
            )

    save_json_atomic(CUSTOMERS_FILE, customers)


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


