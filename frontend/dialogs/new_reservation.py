import customtkinter as ctk
from tkinter import messagebox

from frontend.styles import PRIMARY, TEXT
from storage.json_storage import (
    get_customer_by_dni,
    load_customers,
    load_reservations,
    save_customers,
    save_reservations
)
from frontend.components.validators.reservation_validator import ReservationValidator
from modules.rooms import get_available_rooms
from modules.payments import calculate_igv, calculate_subtotal, calculate_total
from modules.validations import calculate_nights, validate_dni
from frontend.receipt_pdf import generate_receipt, print_receipt

class NewReservationDialog(ctk.CTkToplevel):

    def __init__(self, parent, on_reservation_created=None):

        super().__init__(parent)

        self.title("Nueva Reserva")
        self.geometry("500x700")
        self.resizable(False, False)
        self.configure(fg_color="#F1F5F9")

        self.grab_set()
        self.validator = ReservationValidator()
        self.on_reservation_created = on_reservation_created
        self.create_widgets()

    # =====================================================
    # COMPONENTES
    # =====================================================

    def create_widgets(self):

        # ==========================
        # TÍTULO
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="Nueva Reserva",
            font=("Segoe UI", 25, "bold"),
            text_color=TEXT
        )

        title.pack(
            pady=(22, 4)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Ingresá los datos para gestionar la reserva",
            font=("Segoe UI", 13),
            text_color="#64748B"
        )

        subtitle.pack(
            pady=(0, 18)
        )

        # ==========================
        # FORMULARIO
        # ==========================

        form = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0",
            scrollbar_fg_color="#F1F5F9",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 24)
        )

        # ==========================
        # DNI
        # ==========================

        dni_label = ctk.CTkLabel(
            form,
            text="DNI",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        )

        dni_label.pack(
            anchor="w",
            padx=18,
            pady=(18, 0)
        )

        self.entry_dni = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="#F8FAFC",
            text_color=TEXT,
            placeholder_text="Ingresá el DNI del cliente"
        )

        self.entry_dni.pack(
            fill="x",
            padx=18,
            pady=(6, 2)
        )

        self.dni_error = ctk.CTkLabel(
            form,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.dni_error.pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        # ==========================
        # BOTÓN BUSCAR
        # ==========================

        search_button = ctk.CTkButton(
            form,
            text="Buscar",
            height=42,
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=self.search_customer
        )

        search_button.pack(
            fill="x",
            padx=18,
            pady=(0, 16)
        )

        # ==========================
        # MENSAJE
        # ==========================

        self.message_label = ctk.CTkLabel(
            form,
            text="",
            font=("Segoe UI", 13, "bold"),
            text_color="#64748B"
        )

        self.message_label.pack(
            anchor="w",
            padx=18
        )

        self.form_reservation = ctk.CTkFrame(
            form,
            fg_color="#F8FAFC",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        ctk.CTkLabel(
            self.form_reservation,
            text="Datos de la reserva",
            font=("Segoe UI", 15, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 8)
        )

        ctk.CTkLabel(
            self.form_reservation,
            text="Check In",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=16)

        self.entry_checkin = ctk.CTkEntry(
            self.form_reservation,
            height=40,
            placeholder_text="dd/mm/yyyy",
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color=TEXT
        )
        self.entry_checkin.pack(
            fill="x",
            padx=16,
            pady=(5, 2)
        )
        self.checkin_error = ctk.CTkLabel(
            self.form_reservation,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.checkin_error.pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            self.form_reservation,
            text="Check Out",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=16)

        self.entry_checkout = ctk.CTkEntry(
            self.form_reservation,
            height=40,
            placeholder_text="dd/mm/yyyy",
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color=TEXT
        )
        self.entry_checkout.pack(
            fill="x",
            padx=16,
            pady=(5, 2)
        )
        self.checkout_error = ctk.CTkLabel(
            self.form_reservation,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.checkout_error.pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            self.form_reservation,
            text="Cantidad de huéspedes",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=16)

        self.entry_guests = ctk.CTkEntry(
            self.form_reservation,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color=TEXT,
            placeholder_text="Ej.: 2"
        )
        self.entry_guests.pack(
            fill="x",
            padx=16,
            pady=(5, 2)
        )
        self.guests_error = ctk.CTkLabel(
            self.form_reservation,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.guests_error.pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

        self.continue_button = ctk.CTkButton(
            self.form_reservation,
            text="Continuar",
            height=42,
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=self.continue_reservation
        )
        self.continue_button.pack(
            fill="x",
            padx=16,
            pady=(0, 16)
        )

        self.available_rooms_frame = ctk.CTkFrame(
            self.form_reservation,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#E2E8F0"
        )

        ctk.CTkLabel(
            self.available_rooms_frame,
            text="Habitaciones disponibles",
            font=("Segoe UI", 15, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=14,
            pady=(14, 8)
        )

        self.room_options_frame = ctk.CTkFrame(
            self.available_rooms_frame,
            fg_color="transparent"
        )
        self.room_options_frame.pack(
            fill="x",
            padx=12
        )

        self.room_choice = ctk.IntVar(value=0)

        self.room_selection_error = ctk.CTkLabel(
            self.available_rooms_frame,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.room_selection_error.pack(
            anchor="w",
            padx=14,
            pady=(4, 0)
        )

        self.select_room_button = ctk.CTkButton(
            self.available_rooms_frame,
            text="Seleccionar habitación",
            height=42,
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=self.select_room
        )
        self.select_room_button.pack(
            fill="x",
            padx=14,
            pady=(8, 14)
        )

        self.payment_form = ctk.CTkFrame(
            self.form_reservation,
            fg_color="#F8FAFC",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        ctk.CTkLabel(
            self.payment_form,
            text="Método de pago",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 6)
        )

        self.payment_method = ctk.StringVar(value="")
        for method in ("Efectivo", "Tarjeta"):
            ctk.CTkRadioButton(
                self.payment_form,
                text=method,
                variable=self.payment_method,
                value=method,
                font=("Segoe UI", 12),
                text_color=TEXT,
                fg_color=PRIMARY,
                hover_color="#1D4ED8"
            ).pack(
                anchor="w",
                padx=18,
                pady=4
            )

        ctk.CTkLabel(
            self.payment_form,
            text="Tipo de comprobante",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 6)
        )

        self.receipt_type = ctk.StringVar(value="")
        for receipt in ("Boleta", "Factura"):
            ctk.CTkRadioButton(
                self.payment_form,
                text=receipt,
                variable=self.receipt_type,
                value=receipt,
                font=("Segoe UI", 12),
                text_color=TEXT,
                fg_color=PRIMARY,
                hover_color="#1D4ED8"
            ).pack(
                anchor="w",
                padx=18,
                pady=4
            )

        self.confirm_reservation_button = ctk.CTkButton(
            self.payment_form,
            text="Confirmar reserva",
            height=42,
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=self.confirm_reservation
        )
        self.confirm_reservation_button.pack(
            fill="x",
            padx=16,
            pady=(16, 16)
        )

        self.form_customer = ctk.CTkFrame(
            form,
            fg_color="#F8FAFC",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        ctk.CTkLabel(
            self.form_customer,
            text="Datos del cliente",
            font=("Segoe UI", 15, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 8)
        )

        ctk.CTkLabel(
            self.form_customer,
            text="Nombre",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=16)

        self.entry_name = ctk.CTkEntry(
            self.form_customer,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color=TEXT,
            placeholder_text="Nombre y apellido"
        )
        self.entry_name.pack(
            fill="x",
            padx=16,
            pady=(5, 2)
        )
        self.name_error = ctk.CTkLabel(
            self.form_customer,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.name_error.pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            self.form_customer,
            text="Teléfono",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=16)

        self.entry_phone = ctk.CTkEntry(
            self.form_customer,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color=TEXT,
            placeholder_text="Ingresá un teléfono de contacto"
        )
        self.entry_phone.pack(
            fill="x",
            padx=16,
            pady=(5, 2)
        )
        self.phone_error = ctk.CTkLabel(
            self.form_customer,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        self.phone_error.pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

        self.entry_name.bind("<KeyRelease>", self.validate_name)
        self.entry_phone.bind("<KeyRelease>", self.validate_phone)
        self.entry_checkin.bind("<KeyRelease>", self.validate_checkin)
        self.entry_checkout.bind("<KeyRelease>", self.validate_checkout)
        self.entry_guests.bind("<KeyRelease>", self.validate_guests)

    # =====================================================
    # BUSCAR CLIENTE
    # =====================================================

    def search_customer(self):

        dni = self.entry_dni.get().strip()

        customer = get_customer_by_dni(dni)

        self.form_customer.pack_forget()
        self.form_reservation.pack_forget()

        if customer:

            self.message_label.configure(
                text="✅ Cliente registrado",
                text_color="#22C55E"
            )

        else:

            self.message_label.configure(
                text="❌ Cliente no registrado",
                text_color="#EF4444"
            )

            self.form_customer.pack(
                fill="x",
                padx=18,
                pady=(18, 0)
            )

        self.form_reservation.pack(
            fill="x",
            padx=18,
            pady=(18, 0)
        )

    # =====================================================
    # VALIDACIONES EN TIEMPO REAL
    # =====================================================

    def validate_name(self, event=None):

        valid, message = self.validator.validate_name_field(
            self.entry_name.get()
        )
        self.name_error.configure(text="" if valid else message)

    def validate_phone(self, event=None):

        valid, message = self.validator.validate_phone_field(
            self.entry_phone.get()
        )
        self.phone_error.configure(text="" if valid else message)

    def validate_checkin(self, event=None):

        valid, message = self.validator.validate_check_in(
            self.entry_checkin.get()
        )
        self.checkin_error.configure(text="" if valid else message)

    def validate_checkout(self, event=None):

        valid, message = self.validator.validate_check_out(
            self.entry_checkin.get(),
            self.entry_checkout.get()
        )
        self.checkout_error.configure(text="" if valid else message)

    def validate_guests(self, event=None):

        valid, message = self.validator.validate_guests(
            self.entry_guests.get()
        )
        self.guests_error.configure(text="" if valid else message)

    def continue_reservation(self):

        self.available_rooms_frame.pack_forget()
        self.payment_form.pack_forget()
        self.room_selection_error.configure(text="")
        self.room_choice.set(0)
        self.payment_method.set("")
        self.receipt_type.set("")
        self.selected_room = None
        self.availability_request = None
        self.available_rooms = []

        check_in = self.entry_checkin.get().strip()
        check_out = self.entry_checkout.get().strip()
        guests = self.entry_guests.get().strip()

        check_in_valid, check_in_message = self.validator.validate_check_in(
            check_in
        )
        self.checkin_error.configure(
            text="" if check_in_valid else check_in_message
        )

        check_out_valid, check_out_message = self.validator.validate_check_out(
            check_in,
            check_out
        ) if check_in_valid else (False, "Ingresá un Check In válido.")
        self.checkout_error.configure(
            text="" if check_out_valid else check_out_message
        )

        guests_valid, guests_message = self.validator.validate_guests(guests)
        self.guests_error.configure(
            text="" if guests_valid else guests_message
        )

        if not (check_in_valid and check_out_valid and guests_valid):
            return

        rooms = get_available_rooms(
            int(guests),
            check_in,
            check_out
        )

        if not rooms:
            messagebox.showwarning(
                title="Sin disponibilidad",
                message="No hay habitaciones disponibles para esas fechas.",
                parent=self
            )
            return

        self.available_rooms = rooms
        self.availability_request = (
            check_in,
            check_out,
            int(guests)
        )
        for child in self.room_options_frame.winfo_children():
            child.destroy()

        for room in rooms:
            room_card = ctk.CTkFrame(
                self.room_options_frame,
                fg_color="#F8FAFC",
                corner_radius=8,
                border_width=1,
                border_color="#E2E8F0"
            )
            room_card.pack(
                fill="x",
                pady=(0, 8)
            )

            room_option = ctk.CTkRadioButton(
                room_card,
                text=(
                    f"Habitación {room['number']}\n"
                    f"{room['type']}\n"
                    f"Capacidad: {room['capacity']} · "
                    f"S/{room['price']} por noche"
                ),
                variable=self.room_choice,
                value=room["number"],
                font=("Segoe UI", 12),
                text_color=TEXT,
                fg_color=PRIMARY,
                hover_color="#1D4ED8"
            )
            room_option.pack(
                fill="x",
                padx=12,
                pady=10
            )

        self.available_rooms_frame.pack(
            fill="x",
            padx=16,
            pady=(0, 16)
        )

    def select_room(self):

        selected_number = self.room_choice.get()
        if not selected_number:
            self.room_selection_error.configure(
                text="Seleccioná una habitación para continuar."
            )
            return

        self.selected_room = next(
            room for room in self.available_rooms
            if room["number"] == selected_number
        )
        self.room_selection_error.configure(text="")
        self.message_label.configure(
            text=f"Habitación {selected_number} seleccionada",
            text_color="#22C55E"
        )
        self.payment_form.pack(
            fill="x",
            padx=16,
            pady=(0, 16)
        )

    def confirm_reservation(self):

        customer_dni = self.entry_dni.get().strip()
        if not validate_dni(customer_dni):
            self.dni_error.configure(
                text="El DNI debe contener 8 dígitos numéricos."
            )
            return

        check_in = self.entry_checkin.get().strip()
        check_out = self.entry_checkout.get().strip()
        guests = self.entry_guests.get().strip()
        check_in_valid, check_in_message = self.validator.validate_check_in(
            check_in
        )
        check_out_valid, check_out_message = (
            self.validator.validate_check_out(check_in, check_out)
            if check_in_valid
            else (False, "Ingresá un Check In válido.")
        )
        guests_valid, guests_message = self.validator.validate_guests(guests)
        self.checkin_error.configure(
            text="" if check_in_valid else check_in_message
        )
        self.checkout_error.configure(
            text="" if check_out_valid else check_out_message
        )
        self.guests_error.configure(
            text="" if guests_valid else guests_message
        )
        if not (check_in_valid and check_out_valid and guests_valid):
            return

        if self.availability_request != (check_in, check_out, int(guests)):
            messagebox.showwarning(
                title="Disponibilidad desactualizada",
                message=(
                    "Volvé a presionar Continuar para buscar habitaciones "
                    "con las fechas y cantidad de huéspedes actuales."
                ),
                parent=self
            )
            return

        customer = get_customer_by_dni(customer_dni)
        if customer is None:
            name_valid, name_message = self.validator.validate_name_field(
                self.entry_name.get().strip()
            )
            phone_valid, phone_message = self.validator.validate_phone_field(
                self.entry_phone.get().strip()
            )
            self.name_error.configure(
                text="" if name_valid else name_message
            )
            self.phone_error.configure(
                text="" if phone_valid else phone_message
            )
            if not (name_valid and phone_valid):
                return

            customer = {
                "customer_name": self.entry_name.get().strip(),
                "customer_dni": customer_dni,
                "customer_phone": self.entry_phone.get().strip()
            }

        payment_method = self.payment_method.get()
        receipt_type = self.receipt_type.get()
        if not payment_method or not receipt_type:
            messagebox.showwarning(
                title="Datos incompletos",
                message="Seleccioná el método de pago y el tipo de comprobante.",
                parent=self
            )
            return

        if self.selected_room is None:
            messagebox.showwarning(
                title="Habitación no seleccionada",
                message="Seleccioná una habitación antes de confirmar.",
                parent=self
            )
            return

        current_rooms = get_available_rooms(
            int(guests),
            check_in,
            check_out
        )
        if not any(
            room["number"] == self.selected_room["number"]
            for room in current_rooms
        ):
            messagebox.showwarning(
                title="Habitación no disponible",
                message=(
                    "La habitación seleccionada ya no está disponible. "
                    "Volvé a buscar habitaciones."
                ),
                parent=self
            )
            self.available_rooms_frame.pack_forget()
            self.payment_form.pack_forget()
            self.selected_room = None
            self.availability_request = None
            return

        nights = calculate_nights(check_in, check_out)
        guest_count = int(guests)
        subtotal = calculate_subtotal(self.selected_room["price"], nights)
        igv = calculate_igv(subtotal)

        reservation = {
            "customer_dni": customer_dni,
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "guest_count": guest_count,
            "room_number": self.selected_room["number"],
            "room_type": self.selected_room["type"],
            "payment_method": payment_method.lower(),
            "receipt_type": receipt_type.lower(),
            "subtotal": subtotal,
            "igv": igv,
            "total": calculate_total(subtotal, igv)
        }

        try:
            if get_customer_by_dni(customer_dni) is None:
                customers = load_customers()
                customers.append(customer)
                save_customers(customers)

            reservations = load_reservations()
            reservations.append(reservation)
            save_reservations(reservations)
        except OSError as error:
            messagebox.showerror(
                title="Error al guardar",
                message=f"No se pudo guardar la reserva: {error}",
                parent=self
            )
            return

        if self.on_reservation_created is not None:
            self.on_reservation_created()

        try:
            receipt_path = generate_receipt(reservation, customer)
        except OSError as error:
            messagebox.showerror(
                title="Error al generar comprobante",
                message=(
                    "La reserva se guardó, pero no se pudo generar el PDF: "
                    f"{error}"
                ),
                parent=self
            )
            self.destroy()
            return

        self.show_receipt_actions(receipt_path)
        self.destroy()

    def show_receipt_actions(self, receipt_path):

        receipt_dialog = ctk.CTkToplevel(self.master)
        receipt_dialog.title("Reserva confirmada")
        receipt_dialog.geometry("400x190")
        receipt_dialog.resizable(False, False)
        receipt_dialog.configure(fg_color="#F1F5F9")
        receipt_dialog.transient(self.master)

        ctk.CTkLabel(
            receipt_dialog,
            text="¡Reserva confirmada!",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            receipt_dialog,
            text="El comprobante PDF está listo para imprimir.",
            font=("Segoe UI", 12),
            text_color="#64748B"
        ).pack(pady=(0, 18))

        actions = ctk.CTkFrame(
            receipt_dialog,
            fg_color="transparent"
        )
        actions.pack(fill="x", padx=24)

        ctk.CTkButton(
            actions,
            text="Imprimir",
            height=40,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=lambda: self.print_receipt_file(
                receipt_path,
                receipt_dialog
            )
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            actions,
            text="Cerrar",
            height=40,
            fg_color="#64748B",
            hover_color="#475569",
            command=receipt_dialog.destroy
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

    @staticmethod
    def print_receipt_file(receipt_path, parent):

        try:
            print_receipt(receipt_path)
        except OSError as error:
            messagebox.showerror(
                title="Error al imprimir",
                message=f"No se pudo imprimir el comprobante: {error}",
                parent=parent
            )