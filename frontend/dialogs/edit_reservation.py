from datetime import date, datetime
from tkinter import messagebox

import customtkinter as ctk
from tkcalendar import Calendar

from frontend.components.services.edit_reservation_service import (
    get_available_rooms_for_reservation,
    update_reservation
)
from frontend.styles import PRIMARY, TEXT
from frontend.validators.reservation_validator import ReservationValidator


class EditReservationDialog(ctk.CTkToplevel):

    def __init__(self, parent, reservation_index, reservation, on_saved=None):
        super().__init__(parent)

        self.reservation_index = reservation_index
        self.reservation = reservation
        self.on_saved = on_saved
        self.validator = ReservationValidator()
        self.available_rooms = []
        self.availability_request = None
        self._availability_after_id = None

        self.title("Editar reserva")
        self.geometry("520x680")
        self.resizable(False, False)
        self.configure(fg_color="#F1F5F9")
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self.after_idle(self.search_rooms)

    def _create_widgets(self):
        ctk.CTkLabel(
            self,
            text="Editar reserva",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            self,
            text=(
                f"Reserva de {self.reservation['customer_dni']} · "
                f"Habitación {self.reservation['room_number']}"
            ),
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

        self.entry_checkin = self._create_date_field(
            content,
            "Check In",
            "check_in"
        )
        self.entry_checkin.bind(
            "<KeyRelease>",
            self._schedule_room_search
        )
        self.checkin_error = self._create_error_label(content)
        self.entry_checkout = self._create_date_field(
            content,
            "Check Out",
            "check_out"
        )
        self.entry_checkout.bind(
            "<KeyRelease>",
            self._schedule_room_search
        )
        self.checkout_error = self._create_error_label(content)

        ctk.CTkLabel(
            content,
            text="Cantidad de huéspedes",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=18, pady=(4, 0))

        self.entry_guests = ctk.CTkEntry(
            content,
            height=40,
            placeholder_text="Entre 1 y 4"
        )
        self.entry_guests.insert(0, str(self.reservation["guest_count"]))
        self.entry_guests.pack(fill="x", padx=18, pady=(5, 2))
        self.entry_guests.bind(
            "<KeyRelease>",
            self._schedule_room_search
        )
        self.guests_error = self._create_error_label(content)

        ctk.CTkLabel(
            content,
            text="La disponibilidad se actualiza al cambiar fechas o huéspedes.",
            font=("Segoe UI", 11),
            text_color="#64748B"
        ).pack(anchor="w", padx=18, pady=(0, 14))

        room_header = ctk.CTkFrame(content, fg_color="transparent")
        room_header.pack(fill="x", padx=18, pady=(0, 8))

        ctk.CTkLabel(
            room_header,
            text="Habitaciones disponibles",
            font=("Segoe UI", 15, "bold"),
            text_color=TEXT
        ).pack(side="left")

        self.room_count = ctk.CTkLabel(
            room_header,
            text="",
            font=("Segoe UI", 11),
            text_color="#64748B"
        )
        self.room_count.pack(side="right")

        self.room_choice = ctk.IntVar(value=self.reservation["room_number"])
        self.rooms_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        self.rooms_frame.pack(fill="x", padx=18, pady=(0, 4))

        self.rooms_message = ctk.CTkLabel(
            content,
            text="",
            text_color="#64748B",
            font=("Segoe UI", 12)
        )
        self.rooms_message.pack(anchor="w", padx=18, pady=(0, 10))

        self.room_error = self._create_error_label(content)

        ctk.CTkButton(
            content,
            text="Guardar cambios",
            height=42,
            font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=self.save_changes
        ).pack(fill="x", padx=18, pady=(8, 18))

    def _create_date_field(self, parent, label, reservation_key):
        ctk.CTkLabel(
            parent,
            text=label,
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=18, pady=(12, 0))

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=(5, 2))

        entry = ctk.CTkEntry(
            row,
            height=40,
            placeholder_text="dd/mm/yyyy"
        )
        entry.insert(0, self.reservation[reservation_key])
        entry.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            row,
            text="📅",
            width=42,
            height=40,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=lambda: self._open_date_picker(entry)
        ).pack(side="right", padx=(8, 0))
        return entry

    @staticmethod
    def _create_error_label(parent):
        label = ctk.CTkLabel(
            parent,
            text="",
            font=("Segoe UI", 11),
            text_color="#EF4444"
        )
        label.pack(anchor="w", padx=18, pady=(0, 8))
        return label

    def _open_date_picker(self, entry):
        try:
            selected_date = datetime.strptime(
                entry.get().strip(),
                "%d/%m/%Y"
            ).date()
        except ValueError:
            selected_date = date.today()

        picker = ctk.CTkToplevel(self)
        picker.title("Seleccionar fecha")
        picker.resizable(False, False)
        picker.transient(self)

        calendar = Calendar(
            picker,
            selectmode="day",
            year=selected_date.year,
            month=selected_date.month,
            day=selected_date.day,
            date_pattern="dd/mm/yyyy",
            locale="es_PE"
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
            close_picker()
            self._schedule_room_search()

        calendar.bind("<<CalendarSelected>>", select_date)
        picker.protocol("WM_DELETE_WINDOW", close_picker)
        picker.update_idletasks()
        picker.geometry(
            f"+{self.winfo_rootx() + 60}+{self.winfo_rooty() + 100}"
        )
        picker.grab_set()

    def _schedule_room_search(self, event=None):
        self.availability_request = None
        if self._availability_after_id is not None:
            self.after_cancel(self._availability_after_id)

        for child in self.rooms_frame.winfo_children():
            child.destroy()

        self.room_count.configure(text="")
        self.rooms_message.configure(
            text="Actualizando disponibilidad..."
        )
        self._availability_after_id = self.after(
            350,
            self.search_rooms
        )

    def search_rooms(self):
        self._availability_after_id = None
        check_in = self.entry_checkin.get().strip()
        check_out = self.entry_checkout.get().strip()
        guests = self.entry_guests.get().strip()

        if check_in == self.reservation["check_in"]:
            check_in_valid, check_in_message = True, ""
        else:
            check_in_valid, check_in_message = (
                self.validator.validate_check_in(check_in)
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
            self.availability_request = None
            self.rooms_message.configure(
                text="Ingresá fechas y huéspedes válidos para ver opciones."
            )
            return

        try:
            rooms = get_available_rooms_for_reservation(
                self.reservation_index,
                int(guests),
                check_in,
                check_out
            )
        except OSError as error:
            messagebox.showerror(
                title="Error al buscar habitaciones",
                message=f"No se pudo consultar la disponibilidad: {error}",
                parent=self
            )
            return

        previously_selected_room = self.room_choice.get()
        for child in self.rooms_frame.winfo_children():
            child.destroy()

        self.available_rooms = rooms
        self.availability_request = (check_in, check_out, int(guests))
        available_numbers = {room["number"] for room in rooms}
        self.room_choice.set(
            previously_selected_room
            if previously_selected_room in available_numbers
            else 0
        )

        if not rooms:
            self.room_count.configure(text="0 opciones")
            self.rooms_message.configure(
                text="No hay habitaciones disponibles para esas fechas."
            )
            return

        option_label = (
            "opción disponible"
            if len(rooms) == 1
            else "opciones disponibles"
        )
        self.room_count.configure(
            text=f"{len(rooms)} {option_label}"
        )
        self.rooms_message.configure(text="")
        for room in rooms:
            self._create_room_option(room)

    def _create_room_option(self, room):
        card = ctk.CTkFrame(
            self.rooms_frame,
            fg_color="#F8FAFC",
            corner_radius=10,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.pack(fill="x", pady=(0, 8))

        ctk.CTkRadioButton(
            card,
            text=(
                f"Habitación {room['number']} · {room['type']}\n"
                f"Capacidad para {room['capacity']} huéspedes"
            ),
            variable=self.room_choice,
            value=room["number"],
            text_color=TEXT,
            font=("Segoe UI", 12, "bold"),
            fg_color=PRIMARY,
            hover_color="#1D4ED8"
        ).pack(side="left", fill="x", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            card,
            text=f"S/ {room['price']} / noche",
            text_color="#1D4ED8",
            fg_color="#EFF6FF",
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=6
        ).pack(side="right", padx=12)

    def save_changes(self):
        check_in = self.entry_checkin.get().strip()
        check_out = self.entry_checkout.get().strip()
        guests = self.entry_guests.get().strip()
        guest_count_valid, guest_message = self.validator.validate_guests(
            guests
        )
        self.guests_error.configure(
            text="" if guest_count_valid else guest_message
        )
        if not guest_count_valid:
            return

        check_in_valid, check_in_message = (
            self.validator.validate_check_in(check_in)
            if check_in != self.reservation["check_in"]
            else (True, "")
        )
        check_out_valid, check_out_message = (
            self.validator.validate_check_out(check_in, check_out)
            if check_in_valid
            else (False, "Ingresá un Check In válido.")
        )
        self.checkin_error.configure(
            text="" if check_in_valid else check_in_message
        )
        self.checkout_error.configure(
            text="" if check_out_valid else check_out_message
        )
        if not (check_in_valid and check_out_valid):
            return

        request = (check_in, check_out, int(guests))
        if self.availability_request != request:
            messagebox.showwarning(
                title="Disponibilidad desactualizada",
                message=(
                    "Esperá a que se actualice la disponibilidad antes "
                    "de guardar los cambios."
                ),
                parent=self
            )
            return

        room_number = self.room_choice.get()
        if not room_number:
            self.room_error.configure(
                text="Seleccioná una habitación disponible."
            )
            return

        try:
            update_reservation(
                self.reservation_index,
                check_in,
                check_out,
                int(guests),
                room_number
            )
        except (OSError, ValueError, IndexError) as error:
            messagebox.showerror(
                title="No se pudo actualizar",
                message=str(error),
                parent=self
            )
            return

        if self.on_saved is not None:
            self.on_saved()
        self.destroy()