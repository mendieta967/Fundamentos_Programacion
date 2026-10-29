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
    # CREAR LAYOUT
    # ==========================================

    def create_layout(self):

        # La columna derecha ocupa todo el espacio
        self.grid_columnconfigure(1, weight=1)

        # La fila ocupa toda la ventana
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # CONTENIDO
        # ==========================================

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

        # Vista actual

        self.current_view = None

        # ==========================================
        # SIDEBAR
        # ==========================================

        self.sidebar = Sidebar(self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

    # ==========================================
    # CAMBIAR VISTA
    # ==========================================

    def show_view(self, view_class):

        if self.current_view is not None:

            self.current_view.destroy()

        self.current_view = view_class(self.content)

        self.current_view.pack(
            fill="both",
            expand=True
        )


# ==========================================
# EJECUTAR
# ==========================================

if __name__ == "__main__":

    app = App()

    app.mainloop()