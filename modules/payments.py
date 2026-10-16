# calculamos el precio por noche multiplicando el precio por noche por el número de noches
def calculate_subtotal(price_per_night, nights):
    return price_per_night * nights



# calculamos el IVA dependiendo del método de pago, si es con tarjeta se aplica un 21% de IVA, si es efectivo no se aplica IVA
def calculate_iva(subtotal, payment_method):

    if payment_method == "tarjeta":

        return subtotal * 0.21

    return 0



# calculamos el total sumando el subtotal y el IVA
def calculate_total(subtotal, iva):

    return subtotal + iva

