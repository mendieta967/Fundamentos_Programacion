from modules.customer_status import is_customer_active
from storage.json_storage import load_customers


class CustomerSearchService:

    @staticmethod
    def search(query, status="Todos los estados"):

        query = query.strip().casefold()

        customers = load_customers()

        return [
            customer
            for customer in customers
            if (
                not query
                or any(
                    query in str(customer.get(field, "")).casefold()
                    for field in (
                        "customer_name",
                        "customer_dni",
                        "customer_phone"
                    )
                )
            )
            and (
                status == "Todos los estados"
                or status == "Activo" and is_customer_active(customer)
                or status == "Dado de baja" and not is_customer_active(customer)
            )
        ]