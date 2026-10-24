import customtkinter as ctk

from frontend.components.sidebar import Sidebar
from frontend.styles import *


# ==========================================
# CONFIGURACIÓN
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==========================================
# APP
# ==========================================

class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.configure_window()
        self.create_layout()

    # ==========================================
    # CONFIGURAR VENTANA
    # ==========================================

    def configure_window(self):

        self.title("Hostel Melimer")

        self.geometry("1200x700")

        self.minsize(1000, 650)

    # ==========================================
    # LAYOUT
    # ==========================================

    def create_layout(self):

        # La columna del contenido ocupa el espacio restante
        self.grid_columnconfigure(1, weight=1)

        # La fila ocupa toda la ventana
        self.grid_rowconfigure(0, weight=1)

        # ==========================
        # SIDEBAR
        # ==========================

        self.sidebar = Sidebar(self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        # ==========================
        # CONTENIDO
        # ==========================

        self.content = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND,
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )