import customtkinter as ctk
from tkinter import messagebox

from frontend.components.services.customer_service import CustomerService
from frontend.styles import PRIMARY, TEXT
from frontend.validators.customer_validator import CustomerValidator


class NewCustomerDialog(ctk.CTkToplevel):

    def __init__(self, parent, on_saved=None):

        super().__init__(parent)

        self.title("Nuevo Cliente")
        self.geometry("500x700")
        self.resizable(False, False)
        self.configure(fg_color="#F8FAFC")
        self.transient(parent.winfo_toplevel())
        self.grab_set()
        self.on_saved = on_saved
        self.validator = CustomerValidator()

        self.create_widgets()
        self.after(100, self.entry_name.focus_set)
        self.bind("<Return>", lambda _event: self.save_customer())

    # =====================================================
    # COMPONENTES
    # =====================================================

    def create_widgets(self):

        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------

        ctk.CTkLabel(
            self,
            text="Nuevo Cliente",
            font=("Segoe UI", 25, "bold"),
            text_color=TEXT
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            self,
            text="Ingresá los datos para registrar el cliente",
            font=("Segoe UI", 13),
            text_color="#64748B"
        ).pack(pady=(0, 18))

        # -------------------------------------------------
        # FORMULARIO
        # -------------------------------------------------

        form = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 12)
        )

        # -------------------------------------------------
        # NOMBRE
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Nombre",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 0)
        )

        self.entry_name = ctk.CTkEntry(
            form,
            height=44,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="#F8FAFC",
            text_color=TEXT,
            placeholder_text="Nombre y apellido",
            placeholder_text_color="#94A3B8"
        )

        self.entry_name.pack(
            fill="x",
            padx=18,
            pady=(6, 2)
        )
        self.name_error = self._create_error_label(form)
        self.entry_name.bind(
            "<KeyRelease>",
            lambda _event: self.validate_name()
        )

        # -------------------------------------------------
        # DNI
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="DNI",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 0)
        )

        self.entry_dni = ctk.CTkEntry(
            form,
            height=44,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="#F8FAFC",
            text_color=TEXT,
            placeholder_text="Ingrese el DNI",
            placeholder_text_color="#94A3B8"
        )

        self.entry_dni.pack(
            fill="x",
            padx=18,
            pady=(6, 2)
        )
        self.dni_error = self._create_error_label(form)
        self.entry_dni.bind(
            "<KeyRelease>",
            lambda _event: self.validate_dni()
        )

        # -------------------------------------------------
        # TELÉFONO
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Teléfono",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 0)
        )

        self.entry_phone = ctk.CTkEntry(
            form,
            height=44,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="#F8FAFC",
            text_color=TEXT,
            placeholder_text="Ingrese el teléfono",
            placeholder_text_color="#94A3B8"
        )

        self.entry_phone.pack(
            fill="x",
            padx=18,
            pady=(6, 2)
        )
        self.phone_error = self._create_error_label(form)
        self.entry_phone.bind(
            "<KeyRelease>",
            lambda _event: self.validate_phone()
        )

        ctk.CTkLabel(
            form,
            text="Los datos se guardarán en la ficha del cliente.",
            font=("Segoe UI", 11),
            text_color="#64748B"
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 14)
        )

        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=24,
            pady=(0, 20)
        )

        cancel_button = ctk.CTkButton(
            buttons,
            text="Cancelar",
            height=42,
            corner_radius=8,
            fg_color="#E2E8F0",
            text_color="#0F172A",
            hover_color="#CBD5E1",
            cursor="hand2",
            command=self.destroy
        )

        cancel_button.pack(
            side="left",
            expand=True,
            padx=(0, 8)
        )

        self.save_button = ctk.CTkButton(
            buttons,
            text="Guardar",
            height=42,
            corner_radius=8,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            cursor="hand2",
            command=self.save_customer
        )

        self.save_button.pack(
            side="left",
            expand=True,
            padx=(8, 0)
        )

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

    def validate_name(self):
        valid, message = self.validator.validate_name(
            self.entry_name.get().strip()
        )
        self.name_error.configure(text="" if valid else message)
        return valid

    def validate_dni(self):
        dni = self.entry_dni.get().strip()
        valid, message = self.validator.validate_dni(dni)

        if valid and CustomerService.customer_exists(dni):
            valid = False
            message = "Ya existe un cliente con ese DNI."

        self.dni_error.configure(text="" if valid else message)
        return valid

    def validate_phone(self):
        valid, message = self.validator.validate_phone(
            self.entry_phone.get().strip()
        )
        self.phone_error.configure(text="" if valid else message)
        return valid

    def save_customer(self):
        name = self.entry_name.get().strip()
        dni = self.entry_dni.get().strip()
        phone = self.entry_phone.get().strip()

        name_valid = self.validate_name()
        dni_valid = self.validate_dni()
        phone_valid = self.validate_phone()

        if not (name_valid and dni_valid and phone_valid):
            if not name_valid:
                self.entry_name.focus_set()
            elif not dni_valid:
                self.entry_dni.focus_set()
            else:
                self.entry_phone.focus_set()
            return

        try:
            created, message = CustomerService.create_customer(
                name,
                dni,
                phone
            )
        except OSError as error:
            messagebox.showerror(
                title="Error al guardar",
                message=f"No se pudo guardar el cliente: {error}",
                parent=self
            )
            return

        if not created:
            self.dni_error.configure(text=message)
            self.entry_dni.focus_set()
            return

        if self.on_saved is not None:
            self.on_saved()

        self.destroy()