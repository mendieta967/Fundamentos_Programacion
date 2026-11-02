from storage.json_storage import load_customers


class CustomerSearchService:

    @staticmethod
    def search(query):

        query = query.strip().casefold()

        customers = load_customers()

        if not query:
            return customers

        return [

            customer

            for customer in customers

            if any(
                query in str(customer.get(field, "")).casefold()
                for field in (
                    "customer_name",
                    "customer_dni",
                    "customer_phone"
                )
            )

        ]