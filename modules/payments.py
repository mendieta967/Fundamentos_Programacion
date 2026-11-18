# ==========================================
# IMPUESTO GENERAL A LAS VENTAS (IGV)
# ==========================================

IGV = 0.18


# ==========================================
# CALCULAR SUBTOTAL
# ==========================================

def calculate_subtotal(
    price_per_night,
    nights
):

    return round(price_per_night * nights, 2)


# ==========================================
# CALCULAR IGV
# ==========================================

def calculate_igv(subtotal):

    return round(subtotal * IGV, 2)


# ==========================================
# CALCULAR TOTAL
# ==========================================

def calculate_total(
    subtotal,
    igv
):

    return round(subtotal + igv, 2)