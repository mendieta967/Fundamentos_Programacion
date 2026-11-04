class RoomSearchService:

    @staticmethod
    def search(rooms, query="", status="Todos los estados"):
        normalized_query = query.strip().casefold()

        return [
            room
            for room in rooms
            if (
                not normalized_query
                or normalized_query in str(room["number"]).casefold()
            )
            and (
                status == "Todos los estados"
                or room["status"] == status
            )
        ]
