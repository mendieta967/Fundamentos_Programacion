from datetime import datetime


# Validamos que el nombre no esté vacío y solo contenga letras y espacios
def validate_name(name):

    # Eliminamos espacios al inicio y final
    cleaned_name = name.strip()

    # Verificamos que solo contenga letras y espacios
    return cleaned_name.replace(" ", "").isalpha()


# Validamos que el DNI tenga exactamente 8 dígitos numéricos
def validate_dni(dni):

    return dni.isdigit() and len(dni) == 8


# Validamos que el teléfono tenga exactamente 9 dígitos numéricos
def validate_phone(phone):

    return phone.isdigit() and len(phone) == 9


# Validamos que la fecha tenga formato válido y exista realmente
def validate_date(date):

    try:

        datetime.strptime(date, "%d/%m/%Y")

        return True

    except ValueError:

        return False


# Validamos que la fecha ingresada sea hoy o futura
def validate_future_date(date):

    reservation_date = datetime.strptime(date, "%d/%m/%Y")

    today = datetime.today()

    return reservation_date.date() >= today.date()


# Validamos que la cantidad de huéspedes esté entre 1 y 4
def validate_guest_count(guest_count):

    return guest_count.isdigit() and 1 <= int(guest_count) <= 4


# Calculamos la cantidad de noches entre check-in y check-out
def calculate_nights(check_in, check_out):

    check_in_date = datetime.strptime(check_in, "%d/%m/%Y")

    check_out_date = datetime.strptime(check_out, "%d/%m/%Y")

    nights = (check_out_date - check_in_date).days

    # Si la fecha de salida es igual o menor a la entrada
    if nights <= 0:

        return None

    return nights

def custom_input(message):

    value = input(message)

    if value.lower() == "cancelar":

        print("Reserva cancelada. Gracias por visitarnos.")

        exit()

    return value
