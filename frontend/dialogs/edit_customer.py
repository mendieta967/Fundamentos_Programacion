import customtkinter as ctk

from frontend.dialogs.alerts import messagebox
from frontend.components.services.customer_service import CustomerService
from frontend.styles import PRIMARY, TEXT
from frontend.validators.customer_validator import CustomerValidator


class EditCustomerDialog(ctk.CTkToplevel):

    def __init__(self, parent, customer, on_saved=None):
        super().__init__(parent)

        self.customer = customer
        self.on_saved = on_saved
        self.validator = CustomerValidator()

        self.title("Editar cliente")
        self.geometry("500x700")
        self.resizable(False, False)
        self.configure(fg_color="#F8FAFC")
        self.transient(parent.winfo_toplevel())
        self.grab_set()

        self._create_widgets()
        self.after(100, self.entry_name.focus_set)
        self.bind("<Return>", lambda _event: self.save_changes())

    def _create_widgets(self):
        ctk.CTkLabel(
            self,
            text="Editar Cliente",
            font=("Segoe UI", 25, "bold"),
            text_color=TEXT
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            self,
            text="Actualizá los datos de la ficha del cliente",
            font=("Segoe UI", 13),
            text_color="#64748B"
        ).pack(pady=(0, 18))

        form = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0"
        )
        form.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        self._create_label(form, "Nombre", top_padding=18)
        self.entry_name = self._create_entry(
            form,
            placeholder="Nombre y apellido",
            value=self.customer.get("customer_name", "")
        )
        self.name_error = self._create_error_label(form)
        self.entry_name.bind("<KeyRelease>", lambda _event: self._validate_name())

        self._create_label(form, "DNI")
        self.entry_dni = self._create_entry(
            form,
            placeholder="DNI del cliente",
            value=self.customer.get("customer_dni", ""),
            state="disabled"
        )

        alert = ctk.CTkFrame(
            form,
            fg_color="#FFFBEB",
            corner_radius=9,
            border_width=1,
            border_color="#FDE68A"
        )
        alert.pack(fill="x", padx=18, pady=(8, 18))

        ctk.CTkLabel(
            alert,
            text="!",
            width=28,
            height=28,
            fg_color="#FEF3C7",
            text_color="#B45309",
            corner_radius=14,
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=(10, 8), pady=9)

        ctk.CTkLabel(
            alert,
            text="El DNI no se puede modificar porque identifica "
                 "las reservas asociadas al cliente.",
            font=("Segoe UI", 11),
            text_color="#92400E",
            wraplength=355,
            justify="left"
        ).pack(side="left", fill="x", expand=True, padx=(0, 10), pady=9)

        self._create_label(form, "Teléfono")
        self.entry_phone = self._create_entry(
            form,
            placeholder="Ingrese el teléfono",
            value=self.customer.get("customer_phone", "")
        )
        self.phone_error = self._create_error_label(form)
        self.entry_phone.bind(
            "<KeyRelease>",
            lambda _event: self._validate_phone()
        )

        ctk.CTkLabel(
            form,
            text="Los cambios se aplicarán a la ficha del cliente.",
            font=("Segoe UI", 11),
            text_color="#64748B"
        ).pack(anchor="w", padx=18, pady=(8, 18))

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=(0, 20))

        ctk.CTkButton(
            buttons,
            text="Cancelar",
            height=42,
            corner_radius=8,
            fg_color="#E2E8F0",
            text_color="#0F172A",
            hover_color="#CBD5E1",
            cursor="hand2",
            command=self.destroy
        ).pack(side="left", expand=True, padx=(0, 8))

        self.save_button = ctk.CTkButton(
            buttons,
            text="Guardar cambios",
            height=42,
            corner_radius=8,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            cursor="hand2",
            command=self.save_changes
        )
        self.save_button.pack(side="left", expand=True, padx=(8, 0))

    @staticmethod
    def _create_label(parent, text, top_padding=0):
        ctk.CTkLabel(
            parent,
            text=text,
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(top_padding, 0))

    @staticmethod
    def _create_entry(parent, placeholder, value, state="normal"):
        entry = ctk.CTkEntry(
            parent,
            height=44,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="#F8FAFC",
            text_color=TEXT,
            placeholder_text=placeholder,
            placeholder_text_color="#94A3B8",
            state="normal"
        )
        entry.pack(fill="x", padx=18, pady=(6, 2))
        entry.insert(0, value)
        if state == "disabled":
            entry.configure(state="disabled")
        return entry

    @staticmethod
    def _create_error_label(parent):
        label = ctk.CTkLabel(
            parent,
            text="",
            height=18,
            font=("Segoe UI", 10),
            text_color="#DC2626",
            anchor="w"
        )
        label.pack(fill="x", padx=18, pady=(0, 4))
        return label

    def _validate_name(self):
        valid, message = self.validator.validate_name(
            self.entry_name.get().strip()
        )
        self.name_error.configure(text="" if valid else message)
        return valid

    def _validate_phone(self):
        valid, message = self.validator.validate_phone(
            self.entry_phone.get().strip()
        )
        self.phone_error.configure(text="" if valid else message)
        return valid

    def save_changes(self):
        name_valid = self._validate_name()
        phone_valid = self._validate_phone()
        if not (name_valid and phone_valid):
            (self.entry_name if not name_valid else self.entry_phone).focus_set()
            return

        try:
            updated, message = CustomerService.update_customer(
                self.customer["customer_dni"],
                self.entry_name.get(),
                self.entry_phone.get()
            )
        except (OSError, ValueError) as error:
            messagebox.showerror(
                title="Error al guardar",
                message=f"No se pudo actualizar el cliente: {error}",
                parent=self
            )
            return

        if not updated:
            messagebox.showerror(
                title="No se pudo actualizar",
                message=message,
                parent=self
            )
            return

        if self.on_saved is not None:
            self.on_saved()
        self.destroy()