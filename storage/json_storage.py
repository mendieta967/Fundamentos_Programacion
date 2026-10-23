import json


# ==========================================
# RESERVAS
# ==========================================

def load_reservations():

    with open("data/reservations.json", "r") as file:

        return json.load(file)


def save_reservations(reservations):

    with open("data/reservations.json", "w") as file:

        json.dump(reservations, file, indent=4)


# ==========================================
# CLIENTES
# ==========================================

def load_customers():

    with open("data/customers.json", "r") as file:

        return json.load(file)


def save_customers(customers):

    with open("data/customers.json", "w") as file:

        json.dump(customers, file, indent=4)


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