import math


class RoomValidator:

    @staticmethod
    def validate_price(price):
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or (
                isinstance(price, float)
                and not math.isfinite(price)
            )
            or price <= 0
        ):
            return False, "El precio debe ser un número mayor que cero."

        return True, ""

    @classmethod
    def parse_price(cls, value):
        try:
            price = float(value.strip().replace(",", "."))
        except (AttributeError, ValueError):
            raise ValueError("Ingresá un precio numérico válido.") from None

        valid, message = cls.validate_price(price)
        if not valid:
            raise ValueError(message)

        return price
