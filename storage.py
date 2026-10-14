import json

def load_reservations():

    with open("data/reservations.json", "r") as file:

        return json.load(file)


def save_reservations(reservations):

    with open("data/reservations.json", "w") as file:

        json.dump(reservations, file, indent=4)

def customer_has_reservations(dni):
    reservations = load_reservations()
    for reservation in reservations:
        if reservation["customer_dni"] == dni:
            return True
    return False