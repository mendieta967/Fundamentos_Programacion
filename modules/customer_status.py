def is_customer_active(customer):
    status = str(customer.get("status", "active")).strip().casefold()
    return status not in {
        "inactive",
        "deleted",
        "cancelled",
        "cancelada",
        "baja"
    }
