from pathlib import Path

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

        self.grid_propagate(False)

        self.load_images()

        self.create_widgets()

    # ==========================================
    # CARGAR IMÁGENES
    # ==========================================

    def load_images(self):

        assets = Path(__file__).resolve().parents[1] / "assets"

        # Logo
        logo = Image.open(assets / "logo.png")

        self.logo = ctk.CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(190, 70)
        )

        # Iconos
        self.icon_reserva = ctk.CTkImage(
            Image.open(assets / "icons" / "icon_reserva.png"),
            size=(20, 20)
        )

        self.icon_usuario = ctk.CTkImage(
            Image.open(assets / "icons" / "icon_usuario.png"),
            size=(20, 20)
        )

        self.icon_habitacion = ctk.CTkImage(
            Image.open(assets / "icons" / "icon_habitacion.png"),
            size=(20, 20)
        )

        self.icon_reporte = ctk.CTkImage(
            Image.open(assets / "icons" / "icon_reporte.png"),
            size=(20, 20)
        )

        self.icon_salir = ctk.CTkImage(
            Image.open(assets / "icons" / "icon_salir.png"),
            size=(18, 18)
        )

    # ==========================================
    # COMPONENTES
    # ==========================================

    def create_widgets(self):

        self.grid_columnconfigure(0, weight=1)

        # -------------------------------
        # LOGO
        # -------------------------------

        logo_label = ctk.CTkLabel(
            self,
            image=self.logo,
            text=""
        )

        logo_label.grid(
            row=0,
            column=0,
            pady=(24, 20)
        )

        ctk.CTkFrame(
            self,
            height=1,
            fg_color="#334155",
            corner_radius=0
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 22),
            sticky="ew"
        )

        # -------------------------------
        # BOTONES
        # -------------------------------

        self.create_button(
            "Gestión de Reservas",
            self.icon_reserva,
            2
        )

        self.create_button(
            "Gestión de Clientes",
            self.icon_usuario,
            3
        )

        self.create_button(
            "Gestión de Habitaciones",
            self.icon_habitacion,
            4
        )

        self.create_button(
            "Reportes",
            self.icon_reporte,
            5
        )

        self.grid_rowconfigure(6, weight=1)

        # -------------------------------
        # BOTÓN SALIR
        # -------------------------------

        exit_button = ctk.CTkButton(
            self,
            text="Salir",
            image=self.icon_salir,
            compound="left",
            fg_color="#DC2626",
            hover_color="#B91C1C",
            height=46,
            corner_radius=10,
            font=("Segoe UI", 15, "bold"),
            text_color="white",
            cursor="hand2"
        )

        exit_button.grid(
            row=7,
            column=0,
            padx=16,
            pady=18,
            sticky="ew"
        )

    # ==========================================
    # BOTONES
    # ==========================================

    def create_button(
        self,
        text,
        image,
        row
    ):

        button = ctk.CTkButton(
            self,
            text=text,
            image=image,
            compound="left",
            anchor="w",
            height=46,
            fg_color="transparent",
            hover_color="#334155",
            text_color="white",
            font=("Segoe UI", 13, "bold"),
            corner_radius=10,
            border_spacing=10,
            cursor="hand2"
        )

        button.grid(
            row=row,
            column=0,
            padx=16,
            pady=4,
            sticky="ew"
        )