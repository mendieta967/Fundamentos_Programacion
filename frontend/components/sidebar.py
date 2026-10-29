from pathlib import Path
from frontend.views.reservations import ReservationsView
from frontend.views.customers import CustomersView
from frontend.views.rooms import RoomsView
from frontend.views.reports import ReportsView

import customtkinter as ctk
from PIL import Image

from frontend.styles import *


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=250,
            fg_color=SIDEBAR,
            corner_radius=0
        )
        self.parent = parent
        self.grid_propagate(False)

        self.buttons = {}
        self.active_button = None

        self.load_images()
        self.create_widgets()

    # ==========================================
    # CARGAR IMÁGENES
    # ==========================================

    def load_images(self):

        assets = Path(__file__).resolve().parents[1] / "assets"

        # -------------------------
        # Logo
        # -------------------------

        logo = Image.open(assets / "logo.png")

        self.logo = ctk.CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(190, 70)
        )

        # -------------------------
        # Iconos
        # -------------------------

        self.icon_reserva = ctk.CTkImage(
            light_image=Image.open(assets / "icons" / "icon_reserva.png"),
            dark_image=Image.open(assets / "icons" / "icon_reserva.png"),
            size=(22, 22)
        )

        self.icon_usuario = ctk.CTkImage(
            light_image=Image.open(assets / "icons" / "icon_usuario.png"),
            dark_image=Image.open(assets / "icons" / "icon_usuario.png"),
            size=(22, 22)
        )

        self.icon_habitacion = ctk.CTkImage(
            light_image=Image.open(assets / "icons" / "icon_habitacion.png"),
            dark_image=Image.open(assets / "icons" / "icon_habitacion.png"),
            size=(22, 22)
        )

        self.icon_reporte = ctk.CTkImage(
            light_image=Image.open(assets / "icons" / "icon_reporte.png"),
            dark_image=Image.open(assets / "icons" / "icon_reporte.png"),
            size=(22, 22)
        )

        self.icon_salir = ctk.CTkImage(
            light_image=Image.open(assets / "icons" / "icon_salir.png"),
            dark_image=Image.open(assets / "icons" / "icon_salir.png"),
            size=(20, 20)
        )

    # ==========================================
    # COMPONENTES
    # ==========================================

    def create_widgets(self):

        self.grid_columnconfigure(0, weight=1)

        # -------------------------
        # Logo
        # -------------------------

        logo_label = ctk.CTkLabel(
            self,
            image=self.logo,
            text=""
        )

        logo_label.grid(
            row=0,
            column=0,
            pady=(25, 18)
        )

        # -------------------------
        # Separador
        # -------------------------

        separator = ctk.CTkFrame(
            self,
            height=2,
            fg_color="#334155",
            corner_radius=100
        )

        separator.grid(
            row=1,
            column=0,
            padx=22,
            pady=(0, 25),
            sticky="ew"
        )

        # -------------------------
        # Menú
        # -------------------------

        self.create_button(
            "reservas",
            "Gestión de Reservas",
            self.icon_reserva,
            2,
            ReservationsView
        )

        self.create_button(
            "clientes",
            "Gestión de Clientes",
            self.icon_usuario,
            3,
            CustomersView
        )

        self.create_button(
            "habitaciones",
            "Gestión de Habitaciones",
            self.icon_habitacion,
            4,
            RoomsView
        )

        self.create_button(
            "reportes",
            "Reportes",
            self.icon_reporte,
            5,
            ReportsView
        )

        # Marca el primero como activo

        self.change_view("reservas", ReservationsView)

        # Empuja el botón salir abajo

        self.grid_rowconfigure(6, weight=1)

        # -------------------------
        # Botón salir
        # -------------------------

        exit_button = ctk.CTkButton(
            self,
            text="Salir",
            image=self.icon_salir,
            compound="left",
            height=52,
            fg_color=DANGER,
            hover_color="#DC2626",
            text_color="white",
            font=("Segoe UI", 15, "bold"),
            corner_radius=12,
            border_spacing=14,
            cursor="hand2",
            command=self.master.destroy
        )

        exit_button.grid(
            row=7,
            column=0,
            padx=18,
            pady=20,
            sticky="ew"
        )

    # ==========================================
    # CREAR BOTÓN
    # ==========================================

    def create_button(
        self,
        key,
        text,
        image,
        row,
        view
    ):

        button = ctk.CTkButton(
            self,
            text=text,
            image=image,
            compound="left",
            anchor="w",
            height=52,
            fg_color="transparent",
            hover_color="#334155",
            text_color="white",
            font=("Segoe UI", 14, "bold"),
            corner_radius=12,
            border_spacing=18,
            cursor="hand2",
            command=lambda k=key, v=view: self.change_view(k, v)
        )

        button.grid(
            row=row,
            column=0,
            padx=18,
            pady=6,
            sticky="ew"
        )

        self.buttons[key] = button

    # ==========================================
    # BOTÓN ACTIVO
    # ==========================================

    def set_active(self, key):

        for name, button in self.buttons.items():

            if name == key:

                button.configure(
                    fg_color=PRIMARY,
                    hover_color=PRIMARY,
                    text_color="white"
                )

                self.active_button = button

            else:

                button.configure(
                    fg_color="transparent",
                    hover_color="#334155",
                    text_color="white"
                )
    
    def change_view(self, key, view):

        self.set_active(key)

        self.parent.show_view(view)