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

    return price_per_night * nights


# ==========================================
# CALCULAR IGV
# ==========================================

def calculate_igv(subtotal):

    return subtotal * IGV


# ==========================================
# CALCULAR TOTAL
# ==========================================

def calculate_total(
    subtotal,
    igv
):

    return subtotal + igv