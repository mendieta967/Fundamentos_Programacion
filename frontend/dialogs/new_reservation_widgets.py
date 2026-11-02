import customtkinter as ctk

from frontend.styles import PRIMARY, TEXT


class NewReservationWidgets:

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

        self._create_customer_search(form)
        self._create_reservation_fields(form)
        self._create_room_selection()
        self._create_payment_form()
        self._create_customer_form(form)

    def _create_customer_search(self, form):

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


    def _create_reservation_fields(self, form):

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

        checkin_row = ctk.CTkFrame(
            self.form_reservation,
            fg_color="transparent"
        )
        checkin_row.pack(
            fill="x",
            padx=16,
            pady=(5, 2)
        )
        self.entry_checkin = ctk.CTkEntry(
            checkin_row,
            height=40,
            placeholder_text="dd/mm/yyyy",
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color=TEXT
        )
        self.entry_checkin.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            checkin_row,
            text="📅",
            width=42,
            height=40,
            corner_radius=8,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=lambda: self.open_date_picker(
                self.entry_checkin,
                self.validate_checkin,
                "Check In"
            )
        ).pack(side="right", padx=(8, 0))

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

        checkout_row = ctk.CTkFrame(
            self.form_reservation,
            fg_color="transparent"
        )
        checkout_row.pack(
            fill="x",
            padx=16,
            pady=(5, 2)
        )
        self.entry_checkout = ctk.CTkEntry(
            checkout_row,
            height=40,
            placeholder_text="dd/mm/yyyy",
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color=TEXT
        )
        self.entry_checkout.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            checkout_row,
            text="📅",
            width=42,
            height=40,
            corner_radius=8,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            command=lambda: self.open_date_picker(
                self.entry_checkout,
                self.validate_checkout,
                "Check Out"
            )
        ).pack(side="right", padx=(8, 0))

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


    def _create_room_selection(self):

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


    def _create_payment_form(self):

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


    def _create_customer_form(self, form):

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
