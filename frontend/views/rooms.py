import customtkinter as ctk

from frontend.dialogs.edit_room import EditRoomDialog
from frontend.utils.icons import load_icon
from frontend.components.services.room_search_service import RoomSearchService
from modules.rooms import get_room_current_reservation, get_rooms


class RoomsView(ctk.CTkFrame):

    STATUS_STYLES = {
        "Disponible": ("#DCFCE7", "#166534", "#22C55E"),
        "Ocupada": ("#FEE2E2", "#B91C1C", "#EF4444"),
        "Mantenimiento": ("#FEF3C7", "#B45309", "#F59E0B")
    }

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#F8FAFC")
        self.icon_search = load_icon("icon_search", size=(16, 16))
        self.icon_edit = load_icon("icon_edit")
        self.rooms = []
        self.inventory_error = None
        self._load_rooms()
        self.create_widgets()

    def _load_rooms(self):
        try:
            for number, room in sorted(get_rooms().items()):
                reservation = get_room_current_reservation(number)
                if room["maintenance"]:
                    status = "Mantenimiento"
                elif reservation:
                    status = "Ocupada"
                else:
                    status = "Disponible"

                reservation_dates = (
                    f"{reservation['check_in']} - {reservation['check_out']}"
                    if reservation
                    else "—"
                )
                self.rooms.append({
                    "number": number,
                    "type": room["type"],
                    "capacity": room["capacity"],
                    "price": room["price"],
                    "maintenance": room["maintenance"],
                    "status": status,
                    "reservation_dates": reservation_dates
                })
        except (OSError, ValueError, KeyError) as error:
            self.rooms.clear()
            self.inventory_error = str(error)

    def create_widgets(self):
        self._create_heading()
        self._create_summary()
        self._create_table_section()

    def refresh_inventory(self):
        query = self.search_entry.get()
        selected_status = self.status_filter.get()

        for widget in self.winfo_children():
            widget.destroy()

        self.rooms.clear()
        self.inventory_error = None
        self._load_rooms()
        self.create_widgets()

        self.search_entry.insert(0, query)
        self.status_filter.set(selected_status)
        self.refresh_table()

    def open_edit_room(self, room):
        return EditRoomDialog(
            self,
            room,
            on_saved=self.refresh_inventory
        )

    def _create_heading(self):
        heading = ctk.CTkFrame(self, fg_color="transparent")
        heading.pack(fill="x", padx=35, pady=(26, 18))

        title_block = ctk.CTkFrame(heading, fg_color="transparent")
        title_block.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_block,
            text="Gestión de Habitaciones",
            font=("Segoe UI", 27, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_block,
            text="Controlá la disponibilidad y consultá los detalles del inventario.",
            font=("Segoe UI", 12),
            text_color="#64748B"
        ).pack(anchor="w", pady=(3, 0))


    def _create_summary(self):
        summary = ctk.CTkFrame(self, fg_color="transparent")
        summary.pack(fill="x", padx=35)

        counts = {
            status: sum(room["status"] == status for room in self.rooms)
            for status in self.STATUS_STYLES
        }
        cards = (
            ("Total habitaciones", str(len(self.rooms)), "#2563EB", "Inventario registrado"),
            ("Disponibles", str(counts["Disponible"]), "#16A34A", "Listas para reservar"),
            ("Ocupadas", str(counts["Ocupada"]), "#DC2626", "Con huéspedes"),
            ("Mantenimiento", str(counts["Mantenimiento"]), "#D97706", "Fuera de servicio")
        )

        for title, value, accent, detail in cards:
            self._create_summary_card(summary, title, value, accent, detail)

    @staticmethod
    def _create_summary_card(parent, title, value, accent, detail):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E7EDF5",
            height=106
        )
        card.pack(side="left", fill="both", expand=True, padx=(0, 12))
        card.pack_propagate(False)

        ctk.CTkFrame(
            card,
            width=3,
            fg_color=accent,
            corner_radius=2
        ).pack(side="left", fill="y", padx=(13, 11), pady=16)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, pady=13)

        ctk.CTkLabel(
            content,
            text=title,
            font=("Segoe UI", 11, "bold"),
            text_color="#64748B"
        ).pack(anchor="w")

        value_row = ctk.CTkFrame(content, fg_color="transparent")
        value_row.pack(fill="x", pady=(1, 0))

        ctk.CTkLabel(
            value_row,
            text=value,
            font=("Segoe UI", 25, "bold"),
            text_color="#0F172A"
        ).pack(side="left")

        ctk.CTkLabel(
            content,
            text=detail,
            font=("Segoe UI", 10),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(0, 1))

    def _create_table_section(self):
        section = ctk.CTkFrame(self, fg_color="transparent")
        section.pack(fill="both", expand=True, padx=35, pady=(22, 24))

        section_heading = ctk.CTkFrame(section, fg_color="transparent")
        section_heading.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            section_heading,
            text="Habitaciones registradas",
            font=("Segoe UI", 16, "bold"),
            text_color="#0F172A"
        ).pack(side="left")

        filter_bar = ctk.CTkFrame(
            section,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0",
            height=62
        )
        filter_bar.pack(fill="x", pady=(0, 12))
        filter_bar.pack_propagate(False)

        search_box = ctk.CTkFrame(
            filter_bar,
            fg_color="#F8FAFC",
            corner_radius=9,
            border_width=1,
            border_color="#E2E8F0",
            height=40
        )
        search_box.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(12, 10),
            pady=10
        )
        search_box.pack_propagate(False)

        ctk.CTkLabel(
            search_box,
            text="",
            image=self.icon_search
        ).pack(side="left", padx=(11, 2))

        self.search_entry = ctk.CTkEntry(
            search_box,
            placeholder_text="Buscar por número de habitación...",
            height=36,
            border_width=0,
            corner_radius=8,
            fg_color="transparent",
            text_color="#0F172A",
            placeholder_text_color="#94A3B8",
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 8),
            pady=2
        )
        self.search_entry.bind(
            "<KeyRelease>",
            lambda _event: self.refresh_table()
        )
        self.search_entry.bind(
            "<Return>",
            lambda _event: self.refresh_table()
        )

        filter_label = ctk.CTkLabel(
            filter_bar,
            text="ESTADO",
            font=("Segoe UI", 9, "bold"),
            text_color="#94A3B8"
        )
        filter_label.pack(side="left", padx=(2, 8))

        self.status_filter = ctk.CTkComboBox(
            filter_bar,
            values=["Todos los estados", "Disponible", "Ocupada", "Mantenimiento"],
            width=200,
            height=38,
            state="readonly",
            corner_radius=9,
            border_width=1,
            border_color="#94A3B8",
            fg_color="#FFFFFF",
            text_color="#0F172A",
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#DBEAFE",
            font=("Segoe UI", 11, "bold"),
            dropdown_font=("Segoe UI", 11),
            command=lambda _value: self.refresh_table()
        )
        self.status_filter.configure(cursor="hand2")
        self.status_filter._canvas.configure(cursor="hand2")
        self.status_filter._entry.configure(cursor="hand2")
        self.status_filter._dropdown_menu.configure(cursor="hand2")
        self.status_filter.set("Todos los estados")
        self.status_filter.pack(side="left", padx=(0, 12), pady=10)

        self.table = ctk.CTkScrollableFrame(
            section,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        self.table.pack(fill="both", expand=True)

        self.refresh_table()

    def refresh_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()

        self._create_table_header(self.table)
        if self.inventory_error:
            ctk.CTkLabel(
                self.table,
                text=f"No se pudo cargar el inventario: {self.inventory_error}",
                font=("Segoe UI", 13),
                text_color="#B91C1C",
                wraplength=700
            ).pack(padx=20, pady=28)
            return

        if not self.rooms:
            ctk.CTkLabel(
                self.table,
                text="No hay habitaciones para mostrar.",
                font=("Segoe UI", 13),
                text_color="#64748B"
            ).pack(padx=20, pady=28)
            return

        filtered_rooms = RoomSearchService.search(
            self.rooms,
            self.search_entry.get(),
            self.status_filter.get()
        )
        if not filtered_rooms:
            ctk.CTkLabel(
                self.table,
                text="No se encontraron habitaciones con esos filtros.",
                font=("Segoe UI", 13),
                text_color="#64748B"
            ).pack(padx=20, pady=28)
            return

        for index, room in enumerate(filtered_rooms):
            self._create_room_row(
                self.table,
                room,
                show_separator=index < len(filtered_rooms) - 1
            )

    @staticmethod
    def _create_table_header(parent):
        header = ctk.CTkFrame(
            parent,
            fg_color="#F1F5F9",
            corner_radius=8,
            height=42
        )
        header.pack(fill="x", padx=10, pady=(10, 0))
        header.pack_propagate(False)

        for text, width in (
            ("Habitación", 92),
            ("Tipo", 105),
            ("Capacidad", 100),
            ("Precio / noche", 120),
            ("Estado", 135),
            ("Reserva actual", 145),
            ("Acciones", 88)
        ):
            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                text_color="#64748B"
            ).pack(side="left", padx=4)

        ctk.CTkFrame(
            parent,
            height=1,
            fg_color="#E2E8F0",
            corner_radius=0
        ).pack(fill="x", padx=14)

    def _create_room_row(self, parent, room, show_separator):
        number = room["number"]
        room_type = room["type"]
        capacity = room["capacity"]
        price = room["price"]
        status = room["status"]
        reservation_dates = room["reservation_dates"]
        row = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF" if number % 2 else "#FCFDFE",
            corner_radius=8,
            height=50
        )
        row.pack(fill="x", padx=10, pady=(4, 3))
        row.pack_propagate(False)

        number_badge = ctk.CTkFrame(
            row,
            fg_color="#EFF6FF",
            corner_radius=7,
            width=58,
            height=27
        )
        number_badge.pack(side="left", padx=(8, 34), pady=11)
        number_badge.pack_propagate(False)
        ctk.CTkLabel(
            number_badge,
            text=f"{number}",
            font=("Segoe UI", 11, "bold"),
            text_color="#1D4ED8"
        ).pack(expand=True)

        for text, width, color in (
            (room_type, 105, "#334155"),
            (f"{capacity} huésped{'es' if capacity != 1 else ''}", 100, "#64748B"),
            (f"S/ {price:.2f}", 120, "#0F172A"),
        ):
            ctk.CTkLabel(
                row,
                text=text,
                width=width,
                anchor="w",
                font=("Segoe UI", 11, "bold" if text.startswith("S/") else "normal"),
                text_color=color
            ).pack(side="left", padx=4)

        self._create_status_badge(row, status)

        dates_cell = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=145,
            height=32
        )
        dates_cell.pack(side="left", padx=4)
        dates_cell.pack_propagate(False)

        if reservation_dates == "—":
            ctk.CTkLabel(
                dates_cell,
                text=reservation_dates,
                anchor="w",
                font=("Segoe UI", 10),
                text_color="#94A3B8"
            ).pack(fill="both")
        else:
            dates_badge = ctk.CTkFrame(
                dates_cell,
                fg_color="#EFF6FF",
                corner_radius=6,
                border_width=1,
                border_color="#3B82F6",
                height=27
            )
            dates_badge.pack(anchor="w", pady=2)

            ctk.CTkLabel(
                dates_badge,
                text=reservation_dates,
                font=("Segoe UI", 9, "bold"),
                text_color="#1E40AF"
            ).pack(padx=5, pady=4)

        actions = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=48,
            height=34
        )
        actions.pack(side="left", padx=4)
        actions.pack_propagate(False)

        ctk.CTkButton(
            actions,
            text="",
            image=self.icon_edit,
            width=31,
            height=29,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=8,
            cursor="hand2",
            command=lambda selected_room=room: self.open_edit_room(selected_room)
        ).pack(side="left", padx=(0, 4))

        if show_separator:
            ctk.CTkFrame(
                parent,
                fg_color="#F1F5F9",
                height=1,
                corner_radius=0
            ).pack(fill="x", padx=14)

    def _create_status_badge(self, parent, status):
        background, foreground, dot = self.STATUS_STYLES[status]
        cell = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            width=135,
            height=32
        )
        cell.pack(side="left", padx=4)
        cell.pack_propagate(False)

        badge = ctk.CTkFrame(
            cell,
            fg_color=background,
            corner_radius=9,
            height=26
        )
        badge.pack(anchor="w", pady=3)

        ctk.CTkFrame(
            badge,
            width=7,
            height=7,
            fg_color=dot,
            corner_radius=4
        ).pack(side="left", padx=(9, 5), pady=9)

        ctk.CTkLabel(
            badge,
            text=status,
            font=("Segoe UI", 9, "bold"),
            text_color=foreground
        ).pack(side="left", padx=(0, 9))
