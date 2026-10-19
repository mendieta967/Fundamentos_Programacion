
# Definimos el IGV
IGV = 0.18

# calculamos el precio por noche multiplicando el precio por noche por el número de noches
def calculate_subtotal(price_per_night, nights):
    return price_per_night * nights



# Calculamos el IGV sumando el subtotal y el IGV
def calculate_igv(subtotal):

    return subtotal * IGV



# calculamos el total sumando el subtotal y el IVA
def calculate_total(subtotal, iga):

    return subtotal + iga

