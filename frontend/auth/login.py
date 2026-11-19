from pathlib import Path

import customtkinter as ctk
from PIL import Image

from frontend.auth.admin_auth import validate_admin
from frontend.styles import BACKGROUND, PRIMARY, TEXT


class LoginWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.authenticated = False

        self.title("Iniciar sesión - Hostel Melimer")
        self.geometry("460x510")
        self.minsize(460, 510)
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=BACKGROUND)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel_login)

        self.create_widgets()

    def create_widgets(self):
        card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.86)

        assets = Path(__file__).resolve().parents[1] / "assets"
        logo = Image.open(assets / "logo.png")
        self.logo = ctk.CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(210, 78)
        )

        ctk.CTkLabel(
            card,
            image=self.logo,
            text=""
        ).pack(pady=(22, 8))

        ctk.CTkLabel(
            card,
            text="Ingresá tus credenciales",
            font=("Segoe UI", 12),
            text_color="#64748B"
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            card,
            text="Usuario",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=24)

        self.username_entry = ctk.CTkEntry(
            card,
            height=42,
            placeholder_text="Usuario"
        )
        self.username_entry.pack(fill="x", padx=24, pady=(6, 12))

        ctk.CTkLabel(
            card,
            text="Contraseña",
            font=("Segoe UI", 12, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=24)

        password_row = ctk.CTkFrame(card, fg_color="transparent")
        password_row.pack(fill="x", padx=24, pady=(6, 4))

        self.password_entry = ctk.CTkEntry(
            password_row,
            height=42,
            placeholder_text="Contraseña",
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True)

        self.show_password = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            password_row,
            text="Ver",
            variable=self.show_password,
            command=self.toggle_password,
            width=55,
            font=("Segoe UI", 11)
        ).pack(side="left", padx=(8, 0))

        self.error_label = ctk.CTkLabel(
            card,
            text="",
            text_color="#DC2626",
            font=("Segoe UI", 11)
        )
        self.error_label.pack(anchor="w", padx=24, pady=(4, 8))

        ctk.CTkButton(
            card,
            text="Iniciar sesión",
            height=42,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            font=("Segoe UI", 13, "bold"),
            command=self.login
        ).pack(fill="x", padx=24, pady=(0, 24))

        self.username_entry.bind("<Return>", lambda _event: self.login())
        self.password_entry.bind("<Return>", lambda _event: self.login())

    def cancel_login(self):
        self.destroy()
        self.parent.destroy()

    def toggle_password(self):
        self.password_entry.configure(show="" if self.show_password.get() else "*")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if validate_admin(username, password):
            self.authenticated = True
            self.parent.deiconify()
            self.destroy()
            return

        self.error_label.configure(text="Usuario o contraseña incorrectos.")
        self.password_entry.delete(0, "end")
        self.password_entry.focus_set()
