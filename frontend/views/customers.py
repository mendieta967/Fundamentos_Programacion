import customtkinter as ctk

from frontend.dialogs.alerts import messagebox
from frontend.utils.icons import load_icon
from frontend.dialogs.new_customer import NewCustomerDialog
from frontend.dialogs.edit_customer import EditCustomerDialog
from frontend.components.services.customer_service import CustomerService
from frontend.components.services.customer_search_service import (
    CustomerSearchService
)


class CustomersView(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(fg_color="#F8FAFC")

        # Cargar iconos
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
            text="Gestión de Clientes",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            padx=35,
            pady=(30, 20),
            anchor="w"
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
            placeholder_text="Buscar cliente...",
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
            command=self.refresh_table
        )

        search_button.pack(side="left")
        self.search.bind(
            "<KeyRelease>",
            lambda _event: self.refresh_table()
        )
        self.search.bind("<Return>", lambda _event: self.refresh_table())

        new_button = ctk.CTkButton(
            top,
            text="Nuevo Cliente",
            image=self.icon_add,
            compound="left",
            width=180,
            height=42,
            corner_radius=8,
            cursor="hand2",
            command=self.open_new_customer
        )

        new_button.pack(
            side="right",
            padx=(10, 0)
        )

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

    def open_new_customer(self):
        NewCustomerDialog(self, on_saved=self._customer_created)

    def _customer_created(self):
        self.search.delete(0, "end")
        self.refresh_table()

    def refresh_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()

        self.create_header()

        try:
            customers = CustomerSearchService.search(self.search.get())
        except (OSError, ValueError, KeyError, TypeError) as error:
            ctk.CTkLabel(
                self.table,
                text=f"No se pudieron cargar los clientes: {error}",
                font=("Segoe UI", 13),
                text_color="#B91C1C",
                wraplength=800
            ).pack(pady=28)
            return

        if not customers:
            ctk.CTkLabel(
                self.table,
                text="No se encontraron clientes.",
                font=("Segoe UI", 13),
                text_color="#64748B"
            ).pack(pady=28)
            return

        for index, customer in enumerate(customers):
            self.add_row(
                customer,
                show_separator=index < len(customers) - 1
            )

    def create_header(self):
        header = ctk.CTkFrame(
            self.table,
            fg_color="transparent",
            corner_radius=0,
            height=40,
            border_width=0
        )
        header.pack(fill="x", padx=10, pady=(10, 0))

        for text, width in (
            ("Cliente", 280),
            ("DNI", 160),
            ("Teléfono", 180),
            ("Estado", 130),
            ("Acciones", 170)
        ):
            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="w",
                font=("Segoe UI", 14, "bold"),
                text_color="#0F172A"
            ).pack(side="left", padx=6)

        ctk.CTkFrame(
            self.table,
            height=1,
            fg_color="#CBD5E1",
            corner_radius=0
        ).pack(fill="x", padx=14, pady=(0, 2))

    def add_row(self, customer, show_separator):
        row = ctk.CTkFrame(
            self.table,
            fg_color="transparent",
            corner_radius=0,
            height=46,
            border_width=0
        )
        row.pack(fill="x", padx=10, pady=(4, 2))
        row.pack_propagate(False)

        is_active = CustomerService.is_active(customer)
        for text, width in (
            (customer.get("customer_name", "—").strip() or "—", 280),
            (customer.get("customer_dni", "—"), 160),
            (customer.get("customer_phone", "—"), 180)
        ):
            ctk.CTkLabel(
                row,
                text=str(text),
                width=width,
                anchor="w",
                font=("Segoe UI", 13)
            ).pack(side="left", padx=6)

        status_cell = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=130,
            height=30
        )
        status_cell.pack(side="left", padx=6)
        status_cell.pack_propagate(False)

        ctk.CTkFrame(
            status_cell,
            width=9,
            height=9,
            fg_color="#22C55E" if is_active else "#F97316",
            corner_radius=5
        ).pack(side="left", padx=(0, 7), pady=10)

        ctk.CTkLabel(
            status_cell,
            text="Activo" if is_active else "Dado de baja",
            width=105,
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#166534" if is_active else "#C2410C"
        ).pack(side="left")

        actions_cell = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=170,
            height=34
        )
        actions_cell.pack(side="left", padx=6)
        actions_cell.pack_propagate(False)

        if is_active:
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
                command=lambda: self.open_edit_customer(customer)
            ).pack(side="left", padx=4)

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
                command=lambda: self.deactivate_customer(customer)
            ).pack(side="left", padx=4)
        else:
            ctk.CTkButton(
                actions_cell,
                text="Restaurar",
                width=100,
                height=34,
                fg_color="#16A34A",
                hover_color="#15803D",
                corner_radius=8,
                cursor="hand2",
                command=lambda: self.restore_customer(customer)
            ).pack(side="left", padx=4)

        if show_separator:
            ctk.CTkFrame(
                self.table,
                fg_color="#E5E7EB",
                height=1,
                corner_radius=0
            ).pack(fill="x", padx=14, pady=(0, 2))

    def open_edit_customer(self, customer):
        EditCustomerDialog(
            self,
            customer,
            on_saved=self.refresh_table
        )

    def deactivate_customer(self, customer):
        try:
            active_reservations = CustomerService.get_active_reservations(
                customer["customer_dni"]
            )
        except (OSError, KeyError, ValueError, TypeError) as error:
            messagebox.showerror(
                title="No se pudo verificar las reservas",
                message=(
                    "No se pudo determinar si el cliente tiene reservas "
                    f"activas: {error}"
                ),
                parent=self
            )
            return

        if active_reservations:
            self._show_active_reservations_warning(
                customer,
                len(active_reservations)
            )
            return

        if not self._confirm_customer_status_change(customer, restoring=False):
            return

        try:
            updated, message = CustomerService.deactivate_customer(
                customer["customer_dni"]
            )
        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                title="No se pudo dar de baja",
                message=f"No se pudo actualizar el cliente: {error}",
                parent=self
            )
            return

        if not updated:
            if "reserva activa" in message:
                try:
                    active_count = len(
                        CustomerService.get_active_reservations(
                            customer["customer_dni"]
                        )
                    )
                except (OSError, KeyError, ValueError, TypeError) as error:
                    messagebox.showerror(
                        title="No se pudo verificar las reservas",
                        message=f"No se pudo verificar el estado: {error}",
                        parent=self
                    )
                    return

                if active_count:
                    self._show_active_reservations_warning(
                        customer,
                        active_count
                    )
                else:
                    messagebox.showwarning(
                        title="No se pudo dar de baja",
                        message=message,
                        parent=self
                    )
                return
            messagebox.showerror(
                title="No se pudo dar de baja",
                message=message,
                parent=self
            )
            return

        self.refresh_table()

    def _show_active_reservations_warning(self, customer, reservation_count):
        dialog = ctk.CTkToplevel(self)
        dialog.title("No se puede dar de baja")
        dialog.geometry("490x300")
        dialog.resizable(False, False)
        dialog.configure(fg_color="white")
        dialog.transient(self.winfo_toplevel())

        alert = ctk.CTkFrame(
            dialog,
            fg_color="#FEF2F2",
            corner_radius=12,
            border_width=1,
            border_color="#FEE2E2"
        )
        alert.pack(fill="x", padx=20, pady=(20, 14))

        ctk.CTkLabel(
            alert,
            text="!",
            width=42,
            height=42,
            fg_color="#FEE2E2",
            text_color="#B91C1C",
            corner_radius=21,
            font=("Segoe UI", 24, "bold")
        ).pack(side="left", padx=14, pady=14)

        copy = ctk.CTkFrame(alert, fg_color="transparent")
        copy.pack(side="left", fill="x", expand=True, pady=12)

        ctk.CTkLabel(
            copy,
            text="El cliente tiene reservas activas",
            text_color="#991B1B",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")
        count_label = (
            "1 reserva activa"
            if reservation_count == 1
            else f"{reservation_count} reservas activas"
        )
        ctk.CTkLabel(
            copy,
            text=count_label,
            text_color="#B91C1C",
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            dialog,
            text=(
                f"No se puede dar de baja a "
                f"{customer.get('customer_name', 'este cliente')} "
                f"(DNI {customer['customer_dni']}) mientras tenga "
                f"{count_label}."
            ),
            text_color="#0F172A",
            font=("Segoe UI", 13),
            wraplength=440,
            justify="left"
        ).pack(anchor="w", padx=24, pady=(2, 8))

        ctk.CTkLabel(
            dialog,
            text=(
                "Primero deben finalizarse o cancelarse. La ficha y las "
                "reservas históricas se conservarán."
            ),
            text_color="#64748B",
            font=("Segoe UI", 12),
            wraplength=440,
            justify="left"
        ).pack(anchor="w", padx=24)

        ctk.CTkButton(
            dialog,
            text="Entendido",
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="white",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=dialog.destroy
        ).pack(side="bottom", fill="x", padx=20, pady=20)

        dialog.grab_set()
        dialog.focus_force()

    def restore_customer(self, customer):
        if not self._confirm_customer_status_change(customer, restoring=True):
            return

        try:
            updated, message = CustomerService.restore_customer(
                customer["customer_dni"]
            )
        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                title="No se pudo restaurar",
                message=f"No se pudo actualizar el cliente: {error}",
                parent=self
            )
            return

        if not updated:
            messagebox.showerror(
                title="No se pudo restaurar",
                message=message,
                parent=self
            )
            return

        self.refresh_table()

    def _confirm_customer_status_change(self, customer, restoring):
        title = "Restaurar cliente" if restoring else "Dar de baja al cliente"
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("470x300" if restoring else "490x330")
        dialog.resizable(False, False)
        dialog.configure(fg_color="white")
        dialog.transient(self.winfo_toplevel())

        result = {"confirmed": False}

        def close_dialog(confirmed=False):
            result["confirmed"] = confirmed
            if dialog.winfo_exists():
                dialog.destroy()

        if restoring:
            background = "#F0FDF4"
            border = "#DCFCE7"
            icon_color = "#15803D"
            icon_background = "#DCFCE7"
            title_color = "#166534"
            subtitle_color = "#15803D"
            heading = "Restaurar cliente"
            subtitle = "La ficha volverá a estar activa."
            action_text = "Sí, restaurar"
            action_color = "#16A34A"
            hover_color = "#15803D"
        else:
            background = "#FEF2F2"
            border = "#FEE2E2"
            icon_color = "#B91C1C"
            icon_background = "#FEE2E2"
            title_color = "#991B1B"
            subtitle_color = "#B91C1C"
            heading = "Acción importante"
            subtitle = "El cliente dejará de estar activo."
            action_text = "Sí, dar de baja"
            action_color = "#DC2626"
            hover_color = "#B91C1C"

        alert = ctk.CTkFrame(
            dialog,
            fg_color=background,
            corner_radius=12,
            border_width=1,
            border_color=border
        )
        alert.pack(fill="x", padx=20, pady=(20, 12))

        ctk.CTkLabel(
            alert,
            text="↻" if restoring else "!",
            width=42,
            height=42,
            fg_color=icon_background,
            text_color=icon_color,
            corner_radius=21,
            font=("Segoe UI", 23, "bold")
        ).pack(side="left", padx=14, pady=14)

        copy = ctk.CTkFrame(alert, fg_color="transparent")
        copy.pack(side="left", fill="x", expand=True, pady=12)

        ctk.CTkLabel(
            copy,
            text=heading,
            text_color=title_color,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")
        ctk.CTkLabel(
            copy,
            text=subtitle,
            text_color=subtitle_color,
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(2, 0))

        if restoring:
            details = (
                f"¿Querés volver a habilitar a "
                f"{customer.get('customer_name', 'este cliente')} "
                f"(DNI {customer['customer_dni']})?"
            )
            note = "Podrá volver a utilizarse para nuevas reservas."
        else:
            details = (
                f"¿Dar de baja a {customer.get('customer_name', 'este cliente')} "
                f"(DNI {customer['customer_dni']})?"
            )
            note = (
                "La ficha y sus reservas históricas se conservarán. "
                "No se eliminarán datos."
            )

        ctk.CTkLabel(
            dialog,
            text=details,
            text_color="#0F172A",
            font=("Segoe UI", 14),
            wraplength=430,
            justify="left"
        ).pack(anchor="w", padx=24, pady=(4, 8))
        ctk.CTkLabel(
            dialog,
            text=note,
            text_color="#64748B",
            font=("Segoe UI", 12),
            wraplength=430,
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
            cursor="hand2",
            command=lambda: close_dialog(False)
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(
            actions,
            text=action_text,
            height=40,
            fg_color=action_color,
            hover_color=hover_color,
            text_color="white",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=lambda: close_dialog(True)
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

        dialog.protocol("WM_DELETE_WINDOW", lambda: close_dialog(False))
        dialog.update_idletasks()
        width = 470 if restoring else 490
        height = 300 if restoring else 330
        x = self.winfo_rootx() + (self.winfo_width() - width) // 2
        y = self.winfo_rooty() + (self.winfo_height() - height) // 2
        dialog.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        dialog.grab_set()
        dialog.wait_window()
        return result["confirmed"]
