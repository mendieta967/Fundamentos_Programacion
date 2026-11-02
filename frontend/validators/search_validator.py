from modules.validations import validate_dni


class SearchValidator:

    @staticmethod
    def validate_dni(dni):

        if not validate_dni(dni):
            return False, "El DNI debe contener 8 dígitos."

        return True, ""