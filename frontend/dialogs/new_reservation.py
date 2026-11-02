from datetime import date, datetime
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar

from frontend.styles import PRIMARY, TEXT
from storage.json_storage import get_customer_by_dni
from frontend.validators.reservation_validator import ReservationValidator
from modules.rooms import get_available_rooms
from modules.validations import validate_dni
from frontend.pdf.receipt_pdf import generate_receipt, print_receipt
from frontend.dialogs.new_reservation_widgets import NewReservationWidgets
from frontend.components.services.reservation_service import (
    build_reservation_data,
    persist_reservation
)
from frontend.components.services.customer_service import CustomerService

class NewReservationDialog(NewReservationWidgets, ctk.CTkToplevel):

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
    # BUSCAR CLIENTE
    # =====================================================

    def search_customer(self):

        dni = self.entry_dni.get().strip()

        customer = get_customer_by_dni(dni)

        self.form_customer.pack_forget()
        self.form_reservation.pack_forget()

        if customer:
            if not CustomerService.is_active(customer):
                self.message_label.configure(
                    text="Cliente dado de baja. Restauralo antes de crear reservas.",
                    text_color="#EF4444"
                )
                return

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

    def open_date_picker(self, entry, validate_callback, field_name):
        try:
            selected_date = datetime.strptime(
                entry.get().strip(),
                "%d/%m/%Y"
            ).date()
        except ValueError:
            selected_date = date.today()

        picker = ctk.CTkToplevel(self)
        picker.title(f"Seleccionar {field_name}")
        picker.resizable(False, False)
        picker.transient(self)
        picker.configure(fg_color="#F1F5F9")

        calendar = Calendar(
            picker,
            selectmode="day",
            year=selected_date.year,
            month=selected_date.month,
            day=selected_date.day,
            date_pattern="dd/mm/yyyy",
            locale="es_PE",
            background="white",
            foreground="#0F172A",
            headersbackground="#E2E8F0",
            headersforeground="#334155",
            selectbackground=PRIMARY,
            selectforeground="white",
            normalbackground="white",
            normalforeground="#0F172A",
            weekendbackground="white",
            weekendforeground="#0F172A",
            othermonthbackground="#F8FAFC",
            othermonthforeground="#94A3B8",
            bordercolor="#E2E8F0",
            font=("Segoe UI", 10),
            headersfont=("Segoe UI", 10, "bold")
        )
        calendar.pack(padx=12, pady=12)

        def close_picker():
            if picker.winfo_exists():
                picker.destroy()
            self.grab_set()

        def select_date(event=None):
            selected = calendar.selection_get()
            if selected is None:
                return

            entry.delete(0, "end")
            entry.insert(0, selected.strftime("%d/%m/%Y"))
            validate_callback()
            close_picker()

        calendar.bind("<<CalendarSelected>>", select_date)
        picker.protocol("WM_DELETE_WINDOW", close_picker)
        picker.update_idletasks()
        picker.geometry(
            f"+{self.winfo_rootx() + 80}+{self.winfo_rooty() + 120}"
        )
        picker.grab_set()

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

        try:
            rooms = get_available_rooms(
                int(guests),
                check_in,
                check_out
            )
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror(
                title="Error al buscar habitaciones",
                message=f"No se pudo consultar el inventario: {error}",
                parent=self
            )
            return

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
        if customer is not None and not CustomerService.is_active(customer):
            messagebox.showwarning(
                title="Cliente dado de baja",
                message=(
                    "Restaurá el cliente desde la sección Clientes antes "
                    "de crear una nueva reserva."
                ),
                parent=self
            )
            return

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

        try:
            current_rooms = get_available_rooms(
                int(guests),
                check_in,
                check_out
            )
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror(
                title="Error al confirmar la habitación",
                message=f"No se pudo verificar el inventario: {error}",
                parent=self
            )
            return
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

        guest_count = int(guests)
        reservation = build_reservation_data(
            customer_dni=customer_dni,
            check_in=check_in,
            check_out=check_out,
            guest_count=guest_count,
            selected_room=self.selected_room,
            payment_method=payment_method,
            receipt_type=receipt_type
        )

        try:
            persist_reservation(customer, reservation)
        except (OSError, ValueError) as error:
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
            self.after(100, self.destroy)
            return

        self.show_receipt_actions(receipt_path)
        self.after(100, self.destroy)

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
            text="Se abrirá el comprobante para imprimirlo desde el visor PDF.",
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
            print_requested = print_receipt(receipt_path)
        except OSError as error:
            messagebox.showerror(
                title="Error al imprimir",
                message=f"No se pudo abrir o imprimir el comprobante: {error}",
                parent=parent
            )
            return

        if not print_requested:
            messagebox.showinfo(
                title="Comprobante abierto",
                message=(
                    "Windows no tiene una acción de impresión asociada "
                    "al visor PDF. Imprimí el comprobante desde esa "
                    "aplicación."
                ),
                parent=parent
            )