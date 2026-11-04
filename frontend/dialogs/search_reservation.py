import customtkinter as ctk
from datetime import datetime

from frontend.dialogs.alerts import messagebox
from frontend.styles import TEXT
from frontend.components.services.reservation_search_service import (
    ReservationSearchService
)
from frontend.validators.search_validator import SearchValidator
from modules.reservation_status import is_reservation_cancelled


class SearchReservationDialog(ctk.CTkToplevel):

    def __init__(self, parent, initial_dni=""):

        super().__init__(parent)

        self.title("Buscar Reserva")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(fg_color="#F1F5F9")

        self.grab_set()

        self.create_widgets()
        if initial_dni:
            self.entry_dni.insert(0, initial_dni)
            self.entry_dni.configure(state="disabled")
            self.after_idle(self.search_reservations)

    # =====================================================
    # COMPONENTES
    # =====================================================

    def create_widgets(self):

        # ==========================================
        # TÍTULO
        # ==========================================

        title = ctk.CTkLabel(
            self,
            text="Buscar Reserva",
            font=("Segoe UI", 25, "bold"),
            text_color=TEXT
        )

        title.pack(
            pady=(22, 4)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Buscá las reservas de un cliente mediante su DNI",
            font=("Segoe UI", 13),
            text_color="#64748B"
        )

        subtitle.pack(
            pady=(0, 20)
        )

        # ==========================================
        # CONTENEDOR
        # ==========================================

        container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 24)
        )

        # ==========================================
        # DNI
        # ==========================================

        ctk.CTkLabel(
            container,
            text="DNI",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.entry_dni = ctk.CTkEntry(
            container,
            height=42,
            placeholder_text="Ingresá el DNI"
        )

        self.entry_dni.pack(
            fill="x",
            padx=20
        )

        results_header = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        results_header.pack(
            fill="x",
            padx=20,
            pady=(20, 8)
        )

        ctk.CTkLabel(
            results_header,
            text="Resultados de búsqueda",
            text_color=TEXT,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        self.results_count = ctk.CTkLabel(
            results_header,
            text="",
            text_color="#64748B",
            font=("Segoe UI", 12)
        )
        self.results_count.pack(side="right")

        # ==========================================
        # TABLA
        # ==========================================

        self.table_frame = ctk.CTkScrollableFrame(
            container,
            fg_color="#F8FAFC",
            corner_radius=10,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            self.table_frame,
            text="Las reservas aparecerán aquí.",
            text_color="#64748B",
            font=("Segoe UI", 13)
        ).pack(
            pady=40
        )

    def search_reservations(self):
        dni = self.entry_dni.get().strip()
        is_valid, error_message = SearchValidator.validate_dni(dni)
        if not is_valid:
            messagebox.showwarning(
                title="DNI inválido",
                message=error_message,
                parent=self
            )
            return

        try:
            reservations = ReservationSearchService.search_by_dni(dni)
        except OSError as error:
            messagebox.showerror(
                title="Error al buscar",
                message=f"No se pudieron cargar las reservas: {error}",
                parent=self
            )
            return

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        result_label = (
            "reserva encontrada"
            if len(reservations) == 1
            else "reservas encontradas"
        )
        self.results_count.configure(
            text=f"{len(reservations)} {result_label}"
        )

        if not reservations:
            ctk.CTkLabel(
                self.table_frame,
                text="No se encontraron reservas para ese DNI.",
                text_color="#64748B",
                font=("Segoe UI", 13)
            ).pack(pady=40)
            return

        for reservation in reservations:
            self._create_reservation_card(reservation)

    def _create_reservation_card(self, reservation):
        card = ctk.CTkFrame(
            self.table_frame,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.pack(
            fill="x",
            padx=12,
            pady=(12, 0)
        )

        heading = ctk.CTkFrame(card, fg_color="transparent")
        heading.pack(
            fill="x",
            padx=16,
            pady=(14, 10)
        )

        title = ctk.CTkFrame(heading, fg_color="transparent")
        title.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title,
            text=f"Habitación {reservation['room_number']}",
            text_color=TEXT,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title,
            text=reservation["room_type"],
            text_color="#64748B",
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(2, 0))

        if is_reservation_cancelled(reservation):
            status = "Cancelada"
            status_color = "#C2410C"
            status_background = "#FFF7ED"
        else:
            checkout_date = datetime.strptime(
                reservation["check_out"],
                "%d/%m/%Y"
            ).date()
            is_finished = checkout_date < datetime.today().date()
            status = "Finalizada" if is_finished else "Activa"
            status_color = "#B91C1C" if is_finished else "#15803D"
            status_background = "#FEF2F2" if is_finished else "#F0FDF4"

        summary = ctk.CTkFrame(heading, fg_color="transparent")
        summary.pack(side="right")

        ctk.CTkLabel(
            summary,
            text=f"S/ {reservation['total']:.2f}",
            text_color="#1D4ED8",
            fg_color="#EFF6FF",
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            padx=12,
            pady=6
        ).pack(side="right")

        ctk.CTkLabel(
            summary,
            text=status,
            text_color=status_color,
            fg_color=status_background,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=6
        ).pack(side="right", padx=(0, 8))

        divider = ctk.CTkFrame(
            card,
            height=1,
            fg_color="#E2E8F0",
            corner_radius=0
        )
        divider.pack(fill="x", padx=16)

        details = ctk.CTkFrame(card, fg_color="transparent")
        details.pack(
            fill="x",
            padx=16,
            pady=(10, 14)
        )
        for column in range(3):
            details.grid_columnconfigure(column, weight=1)

        self._create_info_item(
            details,
            "CHECK-IN",
            reservation["check_in"],
            row=0,
            column=0
        )
        self._create_info_item(
            details,
            "CHECK-OUT",
            reservation["check_out"],
            row=0,
            column=1
        )
        self._create_info_item(
            details,
            "ESTADÍA",
            f"{reservation['nights']} noches · "
            f"{reservation['guest_count']} huéspedes",
            row=0,
            column=2
        )

    @staticmethod
    def _create_info_item(parent, title, value, row, column):
        item = ctk.CTkFrame(parent, fg_color="transparent")
        item.grid(row=row, column=column, sticky="w", padx=(0, 8))

        ctk.CTkLabel(
            item,
            text=title,
            text_color="#94A3B8",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            item,
            text=value,
            text_color=TEXT,
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(3, 0))