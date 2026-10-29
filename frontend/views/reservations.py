from pathlib import Path
from datetime import datetime

import customtkinter as ctk
from PIL import Image

from storage.json_storage import load_customers, load_reservations
from frontend.dialogs.new_reservation import NewReservationDialog

class ReservationsView(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(fg_color="#F8FAFC")

        self.load_images()

        self.create_widgets()

    # =====================================================
    # CARGAR ICONOS
    # =====================================================

    def load_images(self):

        assets = Path(__file__).resolve().parents[1] / "assets" / "icons"

        self.icon_search = ctk.CTkImage(
            light_image=Image.open(assets / "icon_search.png"),
            dark_image=Image.open(assets / "icon_search.png"),
            size=(18, 18)
        )

        self.icon_add = ctk.CTkImage(
            light_image=Image.open(assets / "icon_add.png"),
            dark_image=Image.open(assets / "icon_add.png"),
            size=(18, 18)
        )

        self.icon_edit = ctk.CTkImage(
            light_image=Image.open(assets / "icon_edit.png"),
            dark_image=Image.open(assets / "icon_edit.png"),
            size=(18, 18)
        )

        self.icon_delete = ctk.CTkImage(
            light_image=Image.open(assets / "icon_delete.png"),
            dark_image=Image.open(assets / "icon_delete.png"),
            size=(18, 18)
        )

    # =====================================================
    # COMPONENTES
    # =====================================================

    def create_widgets(self):

        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------

        title = ctk.CTkLabel(
            self,
            text="Gestión de Reservas",
            font=("Segoe UI", 28, "bold"),
            text_color="#0F172A"
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 20)
        )

        # -------------------------------------------------
        # BARRA SUPERIOR
        # -------------------------------------------------

        top = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=35
        )

        self.search = ctk.CTkEntry(
            top,
            placeholder_text="Buscar reserva...",
            height=42,
            width=350
        )

        self.search.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        search_button = ctk.CTkButton(
            top,
            text="Buscar",
            image=self.icon_search,
            compound="left",
            width=130,
            height=42,
            corner_radius=8,
            cursor="hand2"
        )

        search_button.pack(side="left")

        new_button = ctk.CTkButton(
            top,
            text="Nueva Reserva",
            image=self.icon_add,
            compound="left",
            width=180,
            height=42,
            corner_radius=8,
            cursor="hand2",
            command=self.open_new_reservation
        )

        new_button.pack(
            side="right",
            padx=(10, 0)
        )

        # -------------------------------------------------
        # TABLA
        # -------------------------------------------------

        self.table = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        self.refresh_table()

    def refresh_table(self):

        for widget in self.table.winfo_children():
            widget.destroy()

        self.create_header()

        customers = {
            customer["customer_dni"]: customer["customer_name"]
            for customer in load_customers()
        }

        reservations = load_reservations()

        for index, reservation in enumerate(reservations):
            check_out = reservation["check_out"]
            status = (
                "Finalizada"
                if datetime.strptime(check_out, "%d/%m/%Y").date() < datetime.today().date()
                else "Activa"
            )

            self.add_row(
                customers.get(reservation["customer_dni"], reservation["customer_dni"]),
                str(reservation["room_number"]),
                datetime.strptime(
                    reservation["check_in"], "%d/%m/%Y"
                ).strftime("%d/%m/%y"),
                datetime.strptime(
                    check_out, "%d/%m/%Y"
                ).strftime("%d/%m/%y"),
                status,
                show_separator=index < len(reservations) - 1
            )

    # =====================================================
    # CABECERA
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self.table,
            fg_color="transparent",
            corner_radius=0,
            height=40,
            border_width=0
        )

        header.pack(
            fill="x",
            padx=10,
            pady=(10, 0)
        )

        columns = [

            ("Cliente", 220),
            ("Habitación", 110),
            ("Check In", 120),
            ("Check Out", 120),
            ("Estado", 100),
            ("Acciones", 120)

        ]

        for text, width in columns:

            label = ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="w",
                font=("Segoe UI", 14, "bold"),
                text_color="#0F172A"
            )

            label.pack(
                side="left",
                padx=6
            )

        header_line = ctk.CTkFrame(
            self.table,
            height=1,
            fg_color="#CBD5E1",
            corner_radius=0
        )
        header_line.pack(
            fill="x",
            padx=14,
            pady=(0, 2)
        )

    # =====================================================
    # FILAS
    # =====================================================

    def add_row(
        self,
        cliente,
        habitacion,
        checkin,
        checkout,
        estado,
        show_separator
    ):

        row = ctk.CTkFrame(
            self.table,
            fg_color="transparent",
            corner_radius=0,
            height=46,
            border_width=0
        )

        row.pack(
            fill="x",
            padx=10,
            pady=(4, 2)
        )
        row.pack_propagate(False)

        values = [

            (cliente, 220),
            (habitacion, 110),
            (checkin, 120),
            (checkout, 120)

        ]

        for text, width in values:

            label = ctk.CTkLabel(
                row,
                text=text,
                width=width,
                anchor="w",
                font=("Segoe UI", 13)
            )

            label.pack(
                side="left",
                padx=6
            )

        status_cell = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=100,
            height=30
        )
        status_cell.pack(
            side="left",
            padx=6
        )
        status_cell.pack_propagate(False)

        status_dot = ctk.CTkFrame(
            status_cell,
            width=9,
            height=9,
            fg_color="#EF4444" if estado == "Finalizada" else "#22C55E",
            corner_radius=5
        )
        status_dot.pack(
            side="left",
            padx=(0, 7),
            pady=10
        )

        status_label = ctk.CTkLabel(
            status_cell,
            text=estado,
            width=75,
            anchor="w",
            font=("Segoe UI", 13)
        )
        status_label.pack(side="left")

        # -------------------------
        # EDITAR
        # -------------------------

        actions_cell = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=120,
            height=34
        )
        actions_cell.pack(
            side="left",
            padx=6
        )
        actions_cell.pack_propagate(False)

        edit_button = ctk.CTkButton(
            actions_cell,
            text="",
            image=self.icon_edit,
            width=36,
            height=34,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=8,
            cursor="hand2"
        )

        edit_button.pack(
            side="left",
            padx=(5, 4)
        )

        # -------------------------
        # ELIMINAR
        # -------------------------

        delete_button = ctk.CTkButton(
            actions_cell,
            text="",
            image=self.icon_delete,
            width=36,
            height=34,
            fg_color="#EF4444",
            hover_color="#DC2626",
            corner_radius=8,
            cursor="hand2"
        )

        delete_button.pack(
            side="left",
            padx=(4, 0)
        )

        if show_separator:
            line = ctk.CTkFrame(
                self.table,
                fg_color="#E5E7EB",
                height=1,
                corner_radius=0
            )
            line.pack(
                fill="x",
                padx=14,
                pady=(0, 2)
            )

    def open_new_reservation(self):

        NewReservationDialog(
            self,
            on_reservation_created=self.refresh_table
        )