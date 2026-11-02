from datetime import date, datetime

from modules.reservation_status import is_reservation_cancelled
from modules.customer_status import is_customer_active
from storage.json_storage import (
    load_customers,
    load_reservations,
    save_customers,
    get_customer_by_dni
)


class CustomerService:

    @staticmethod
    def is_active(customer):
        return is_customer_active(customer)

    @staticmethod
    def customer_exists(dni):
        return get_customer_by_dni(dni.strip()) is not None

    @staticmethod
    def create_customer(name, dni, phone):
        name = name.strip()
        dni = dni.strip()
        phone = phone.strip()

        if CustomerService.customer_exists(dni):
            return False, "Ya existe un cliente con ese DNI."

        customers = load_customers()

        customers.append({
            "customer_name": name,
            "customer_dni": dni,
            "customer_phone": phone
        })

        save_customers(customers)

        return True, "Cliente registrado correctamente."

    @staticmethod
    def update_customer(dni, name, phone):
        dni = dni.strip()
        name = name.strip()
        phone = phone.strip()
        customers = load_customers()

        for customer in customers:
            if customer.get("customer_dni") == dni:
                if not CustomerService.is_active(customer):
                    return False, "Restaurá el cliente antes de editarlo."
                customer["customer_name"] = name
                customer["customer_phone"] = phone
                save_customers(customers)
                return True, "Cliente actualizado correctamente."

        return False, "No se encontró el cliente para actualizar."

    @staticmethod
    def get_active_reservations(dni):
        dni = dni.strip()
        today = date.today()
        active = []

        for reservation in load_reservations():
            if (
                reservation.get("customer_dni") != dni
                or is_reservation_cancelled(reservation)
            ):
                continue

            check_out = datetime.strptime(
                reservation["check_out"],
                "%d/%m/%Y"
            ).date()
            if check_out >= today:
                active.append(reservation)

        return active

    @staticmethod
    def deactivate_customer(dni):
        active_reservations = CustomerService.get_active_reservations(dni)
        if active_reservations:
            count = len(active_reservations)
            label = "reserva activa" if count == 1 else "reservas activas"
            return False, (
                f"No se puede dar de baja: el cliente tiene "
                f"{count} {label}. Primero deben finalizarse o cancelarse."
            )

        return CustomerService._set_customer_status(dni, "inactive")

    @staticmethod
    def restore_customer(dni):
        return CustomerService._set_customer_status(dni, "active")

    @staticmethod
    def _set_customer_status(dni, status):
        dni = dni.strip()
        customers = load_customers()

        for customer in customers:
            if customer.get("customer_dni") != dni:
                continue

            if status == "inactive" and not CustomerService.is_active(customer):
                return False, "Este cliente ya está dado de baja."
            if status == "active" and CustomerService.is_active(customer):
                return False, "Este cliente ya está activo."

            customer["status"] = status
            save_customers(customers)
            return True, (
                "Cliente dado de baja correctamente."
                if status == "inactive"
                else "Cliente restaurado correctamente."
            )

        return False, "No se encontró el cliente."