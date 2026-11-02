from modules.validations import (
    validate_name,
    validate_dni,
    validate_phone
)


class CustomerValidator:

    @staticmethod
    def validate_name(name):

        if not validate_name(name):
            return False, "Nombre inválido."

        return True, ""

    @staticmethod
    def validate_dni(dni):

        if not validate_dni(dni):
            return False, "El DNI debe contener 8 dígitos."

        return True, ""

    @staticmethod
    def validate_phone(phone):

        if not validate_phone(phone):
            return False, "El teléfono debe contener 9 dígitos."

        return True, ""