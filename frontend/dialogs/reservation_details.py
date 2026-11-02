import customtkinter as ctk

from frontend.styles import TEXT


class ReservationDetailsDialog(ctk.CTkToplevel):

    def __init__(self, parent, reservation, customer, status):
        super().__init__(parent)

        self.title("Detalle de reserva")
        self.geometry("560x650")
        self.resizable(False, False)
        self.configure(fg_color="#F1F5F9")
        self.transient(parent.winfo_toplevel())
        self.grab_set()

        self._create_widgets(reservation, customer, status)

    def _create_widgets(self, reservation, customer, status):
        ctk.CTkLabel(
            self,
            text="Detalle de reserva",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            self,
            text=f"Reserva de {customer.get('customer_name', 'Cliente no encontrado')}",
            font=("Segoe UI", 13),
            text_color="#64748B"
        ).pack(pady=(0, 14))

        content = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0"
        )
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._add_section(content, "Datos del cliente")
        self._add_detail(content, "Nombre", customer.get("customer_name", "—"))
        self._add_detail(content, "DNI", reservation["customer_dni"])
        self._add_detail(content, "Teléfono", customer.get("customer_phone", "—"))

        self._add_section(content, "Estadía")
        self._add_detail(content, "Estado", status)
        self._add_detail(content, "Check In", reservation["check_in"])
        self._add_detail(content, "Check Out", reservation["check_out"])
        self._add_detail(content, "Noches", reservation["nights"])
        self._add_detail(content, "Huéspedes", reservation["guest_count"])

        self._add_section(content, "Habitación y pago")
        self._add_detail(content, "Habitación", reservation["room_number"])
        self._add_detail(content, "Tipo", reservation["room_type"])
        self._add_detail(
            content,
            "Método de pago",
            str(reservation.get("payment_method") or "—").capitalize()
        )
        self._add_detail(
            content,
            "Comprobante",
            str(reservation.get("receipt_type") or "—").capitalize()
        )

        self._add_section(content, "Importes")
        self._add_detail(content, "Subtotal", f"S/ {reservation['subtotal']:.2f}")
        self._add_detail(content, "IGV", f"S/ {reservation['igv']:.2f}")
        self._add_detail(
            content,
            "Total",
            f"S/ {reservation['total']:.2f}",
            emphasized=True
        )

        ctk.CTkButton(
            content,
            text="Cerrar",
            height=40,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.destroy
        ).pack(fill="x", padx=16, pady=(16, 18))

    @staticmethod
    def _add_section(parent, title):
        ctk.CTkLabel(
            parent,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=16, pady=(16, 6))

    @staticmethod
    def _add_detail(parent, label, value, emphasized=False):
        row = ctk.CTkFrame(
            parent,
            fg_color="#EFF6FF" if emphasized else "#F8FAFC",
            corner_radius=8
        )
        row.pack(fill="x", padx=16, pady=3)

        ctk.CTkLabel(
            row,
            text=label,
            font=("Segoe UI", 12, "bold" if emphasized else "normal"),
            text_color="#64748B",
            anchor="w"
        ).pack(side="left", padx=12, pady=8)

        ctk.CTkLabel(
            row,
            text=str(value),
            font=("Segoe UI", 12, "bold" if emphasized else "normal"),
            text_color="#1D4ED8" if emphasized else TEXT,
            anchor="e"
        ).pack(side="right", padx=12, pady=8)
