import json


# ==========================================
# RUTAS DE LOS ARCHIVOS
# ==========================================

RESERVATIONS_FILE = "data/reservations.json"
CUSTOMERS_FILE = "data/customers.json"


# ==========================================
# RESERVAS
# ==========================================

def load_reservations():

    try:

        with open(RESERVATIONS_FILE, "r") as file:

            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        return []


def save_reservations(reservations):

    with open(RESERVATIONS_FILE, "w") as file:

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

        with open(CUSTOMERS_FILE, "r") as file:

            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        return []


def save_customers(customers):

    with open(CUSTOMERS_FILE, "w") as file:

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