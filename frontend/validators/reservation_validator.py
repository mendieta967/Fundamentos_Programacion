from modules.validations import (
    validate_name,
    validate_phone,
    validate_date,
    validate_future_date,
    validate_guest_count,
    calculate_nights
)


class ReservationValidator:

    # ==========================================
    # NOMBRE
    # ==========================================

    @staticmethod
    def validate_name_field(name):

        if not validate_name(name):
            return False, "Nombre inválido."

        return True, ""

    # ==========================================
    # TELÉFONO
    # ==========================================

    @staticmethod
    def validate_phone_field(phone):

        if not validate_phone(phone):
            return False, "El teléfono debe contener 9 dígitos."

        return True, ""

    # ==========================================
    # CHECK IN
    # ==========================================

    @staticmethod
    def validate_check_in(check_in):

        if not validate_date(check_in):
            return False, "Fecha inválida."

        if not validate_future_date(check_in):
            return False, "La fecha debe ser posterior a hoy."

        return True, ""

    # ==========================================
    # CHECK OUT
    # ==========================================

    @staticmethod
    def validate_check_out(check_in, check_out):

        if not validate_date(check_out):
            return False, "Fecha inválida."

        nights = calculate_nights(
            check_in,
            check_out
        )

        if nights is None:
            return False, "Debe ser posterior al Check In."

        return True, ""

    # ==========================================
    # HUÉSPEDES
    # ==========================================

    @staticmethod
    def validate_guests(guests):

        if not validate_guest_count(guests):
            return False, "Debe ser entre 1 y 4 huéspedes."

        return True, ""