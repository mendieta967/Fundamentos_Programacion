from datetime import datetime

import customtkinter as ctk

from frontend.dialogs.alerts import messagebox
from frontend.utils.icons import load_icon
from storage.json_storage import (
    get_customer_by_dni,
    load_customers,
    load_reservations
)
from frontend.dialogs.new_reservation import NewReservationDialog
from frontend.dialogs.edit_reservation import EditReservationDialog
from frontend.dialogs.reservation_details import ReservationDetailsDialog
from frontend.dialogs.search_reservation import SearchReservationDialog
from frontend.validators.search_validator import SearchValidator
from frontend.components.services.reservation_service import (
    cancel_reservation
)
from modules.reservation_status import is_reservation_cancelled
from frontend.pdf.receipt_pdf import generate_receipt, print_receipt

class ReservationsView(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(fg_color="#F8FAFC")

        self.icon_search = load_icon("icon_search")
        self.icon_add = load_icon("icon_add")
        self.icon_edit = load_icon("icon_edit")
        self.icon_delete = load_icon("icon_delete")

        self.create_widgets()

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
            placeholder_text="Ingresá el DNI del cliente...",
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
            cursor="hand2",
            command=self.open_search_reservation
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

        try:
            customers = {
                customer["customer_dni"]: customer["customer_name"]
                for customer in load_customers()
            }
            reservations = load_reservations()
        except (OSError, ValueError, KeyError, TypeError) as error:
            ctk.CTkLabel(
                self.table,
                text=f"No se pudieron cargar las reservas: {error}",
                font=("Segoe UI", 13),
                text_color="#B91C1C",
                wraplength=800
            ).pack(padx=20, pady=28)
            return

        for index, reservation in enumerate(reservations):
            check_out = reservation["check_out"]
            if is_reservation_cancelled(reservation):
                status = "Cancelada"
            else:
                status = (
                    "Finalizada"
                    if datetime.strptime(
                        check_out,
                        "%d/%m/%Y"
                    ).date() < datetime.today().date()
                    else "Activa"
                )

            self.add_row(
                customers.get(reservation["customer_dni"], reservation["customer_dni"]),
                reservation["customer_dni"],
                str(reservation["room_number"]),
                datetime.strptime(
                    reservation["check_in"], "%d/%m/%Y"
                ).strftime("%d/%m/%y"),
                datetime.strptime(
                    check_out, "%d/%m/%Y"
                ).strftime("%d/%m/%y"),
                status,
                reservation_index=index,
                reservation=reservation,
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

            ("Cliente", 200),
            ("DNI", 130),
            ("Habitación", 110),
            ("Check In", 120),
            ("Check Out", 120),
            ("Estado", 100),
            ("Acciones", 260)

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
        dni,
        habitacion,
        checkin,
        checkout,
        estado,
        reservation_index,
        reservation,
        show_separator
    ):
        is_cancelled = is_reservation_cancelled(reservation)

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

            (cliente, 200),
            (dni, 130),
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
            fg_color=(
                "#F97316"
                if is_cancelled
                else "#EF4444"
                if estado == "Finalizada"
                else "#22C55E"
            ),
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

        actions_cell = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=260,
            height=34
        )
        actions_cell.pack(
            side="left",
            padx=6
        )
        actions_cell.pack_propagate(False)

        ctk.CTkButton(
            actions_cell,
            text="Ver",
            width=44,
            height=34,
            fg_color="#475569",
            hover_color="#334155",
            corner_radius=8,
            cursor="hand2",
            command=lambda: self.open_reservation_details(
                reservation,
                estado
            )
        ).pack(side="left", padx=(2, 4))

        ctk.CTkButton(
            actions_cell,
            text="Imprimir",
            width=68,
            height=34,
            fg_color="#0F766E",
            hover_color="#115E59",
            corner_radius=8,
            cursor="hand2",
            command=lambda: self.print_reservation(reservation, estado)
        ).pack(side="left", padx=4)

        if is_cancelled:
            ctk.CTkButton(
                actions_cell,
                text="Reprogramar",
                width=94,
                height=34,
                fg_color="#16A34A",
                hover_color="#15803D",
                corner_radius=8,
                cursor="hand2",
                command=lambda: self.open_edit_reservation(
                    reservation_index,
                    reservation,
                    rebooking=True
                )
            ).pack(side="left", padx=4)
        if not is_cancelled and estado != "Finalizada":
            ctk.CTkButton(
                actions_cell,
                text="",
                image=self.icon_edit,
                width=36,
                height=34,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                corner_radius=8,
                cursor="hand2",
                command=lambda: self.open_edit_reservation(
                    reservation_index,
                    reservation
                )
            ).pack(side="left", padx=4)

        if not is_cancelled and estado != "Finalizada":
            ctk.CTkButton(
                actions_cell,
                text="",
                image=self.icon_delete,
                width=36,
                height=34,
                fg_color="#EF4444",
                hover_color="#DC2626",
                corner_radius=8,
                cursor="hand2",
                command=lambda: self.cancel_reservation(
                    reservation_index,
                    reservation
                )
            ).pack(side="left", padx=(4, 0))

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

    def open_edit_reservation(
        self,
        reservation_index,
        reservation,
        rebooking=False
    ):
        EditReservationDialog(
            self,
            reservation_index,
            reservation,
            on_saved=self.refresh_table,
            rebooking=rebooking
        )

    def open_reservation_details(self, reservation, status):
        customer = get_customer_by_dni(reservation["customer_dni"]) or {}
        ReservationDetailsDialog(
            self,
            reservation,
            customer,
            status
        )

    def print_reservation(self, reservation, status):
        try:
            customer = get_customer_by_dni(reservation["customer_dni"])
        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                title="No se pudo cargar el cliente",
                message=f"No se pudo leer el archivo de clientes: {error}",
                parent=self
            )
            return

        if customer is None:
            messagebox.showerror(
                title="Cliente no encontrado",
                message=(
                    "No se puede generar el comprobante porque no se "
                    "encontraron los datos del cliente."
                ),
                parent=self
            )
            return

        try:
            printable_reservation = dict(reservation)
            printable_reservation["display_status"] = status
            receipt_path = generate_receipt(
                printable_reservation,
                customer
            )
            print_requested = print_receipt(receipt_path)
        except OSError as error:
            messagebox.showerror(
                title="No se pudo imprimir",
                message=f"No se pudo generar o abrir el comprobante: {error}",
                parent=self
            )
            return

        if not print_requested:
            messagebox.showinfo(
                title="Comprobante abierto",
                message=(
                    "Windows no tiene una acción de impresión asociada "
                    "al visor PDF. Se abrió el comprobante; imprimilo "
                    "desde esa aplicación."
                ),
                parent=self
            )

    def cancel_reservation(self, reservation_index, reservation):
        if not self._confirm_cancel_reservation(reservation):
            return

        try:
            cancel_reservation(reservation_index)
        except (OSError, ValueError, IndexError) as error:
            messagebox.showerror(
                title="No se pudo cancelar",
                message=str(error),
                parent=self
            )
            return

        self.refresh_table()

    def _confirm_cancel_reservation(self, reservation):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Cancelar reserva")
        dialog.geometry("460x300")
        dialog.resizable(False, False)
        dialog.configure(fg_color="white")
        dialog.transient(self.winfo_toplevel())

        result = {"confirmed": False}

        def close_dialog(confirmed=False):
            result["confirmed"] = confirmed
            if dialog.winfo_exists():
                dialog.destroy()

        warning_header = ctk.CTkFrame(
            dialog,
            fg_color="#FEF2F2",
            corner_radius=12
        )
        warning_header.pack(fill="x", padx=20, pady=(20, 12))

        ctk.CTkLabel(
            warning_header,
            text="!",
            width=42,
            height=42,
            fg_color="#FEE2E2",
            text_color="#B91C1C",
            corner_radius=21,
            font=("Segoe UI", 24, "bold")
        ).pack(side="left", padx=14, pady=14)

        warning_copy = ctk.CTkFrame(
            warning_header,
            fg_color="transparent"
        )
        warning_copy.pack(side="left", fill="x", expand=True, pady=12)

        ctk.CTkLabel(
            warning_copy,
            text="Acción importante",
            text_color="#991B1B",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            warning_copy,
            text="La reserva dejará de estar activa.",
            text_color="#B91C1C",
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            dialog,
            text=(
                f"¿Cancelar la reserva de {reservation['customer_dni']} "
                f"para la habitación {reservation['room_number']}?"
            ),
            text_color="#0F172A",
            font=("Segoe UI", 14),
            wraplength=410,
            justify="left"
        ).pack(anchor="w", padx=24, pady=(4, 8))

        ctk.CTkLabel(
            dialog,
            text=(
                "Se conservará en el historial y la habitación quedará "
                "disponible para esas fechas."
            ),
            text_color="#64748B",
            font=("Segoe UI", 12),
            wraplength=410,
            justify="left"
        ).pack(anchor="w", padx=24)

        actions = ctk.CTkFrame(dialog, fg_color="transparent")
        actions.pack(side="bottom", fill="x", padx=20, pady=20)

        ctk.CTkButton(
            actions,
            text="No, volver",
            height=40,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#334155",
            command=lambda: close_dialog(False)
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            actions,
            text="Sí, cancelar reserva",
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white",
            font=("Segoe UI", 12, "bold"),
            command=lambda: close_dialog(True)
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

        dialog.protocol("WM_DELETE_WINDOW", lambda: close_dialog(False))
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 460) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 300) // 2
        dialog.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        dialog.grab_set()
        dialog.wait_window()
        return result["confirmed"]

    def open_search_reservation(self):
        dni = self.search.get().strip()
        is_valid, error_message = SearchValidator.validate_dni(dni)
        if not is_valid:
            messagebox.showwarning(
                title="DNI inválido",
                message=error_message,
                parent=self
            )
            return

        SearchReservationDialog(
            self,
            initial_dni=dni
        )