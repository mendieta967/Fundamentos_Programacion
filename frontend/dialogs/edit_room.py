import customtkinter as ctk

from frontend.dialogs.alerts import messagebox
from frontend.styles import PRIMARY, TEXT
from frontend.validators.room_validator import RoomValidator
from modules.rooms import update_room_details


class EditRoomDialog(ctk.CTkToplevel):

    def __init__(self, parent, room, on_saved=None):
        super().__init__(parent)

        self.room = room
        self.on_saved = on_saved
        self.title(f"Editar habitación {room['number']}")
        self.geometry("460x470")
        self.resizable(False, False)
        self.configure(fg_color="#F8FAFC")
        self.transient(parent.winfo_toplevel())
        self.grab_set()

        self._create_widgets()
        self.after(100, self.price_entry.focus_set)
        self.bind("<Return>", lambda _event: self.save_changes())

    def _create_widgets(self):
        ctk.CTkLabel(
            self,
            text=f"Editar habitación {self.room['number']}",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            self,
            text=f"{self.room['type']} · Capacidad para "
                 f"{self.room['capacity']} huéspedes",
            font=("Segoe UI", 12),
            text_color="#64748B"
        ).pack(pady=(0, 18))

        form = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0"
        )
        form.pack(fill="both", expand=True, padx=24, pady=(0, 14))

        ctk.CTkLabel(
            form,
            text="Precio por noche",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(20, 0))

        price_field = ctk.CTkFrame(
            form,
            fg_color="#F8FAFC",
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1",
            height=44
        )
        price_field.pack(fill="x", padx=18, pady=(7, 4))
        price_field.pack_propagate(False)

        ctk.CTkLabel(
            price_field,
            text="S/",
            font=("Segoe UI", 13, "bold"),
            text_color="#64748B"
        ).pack(side="left", padx=(12, 4))

        self.price_entry = ctk.CTkEntry(
            price_field,
            height=40,
            border_width=0,
            fg_color="transparent",
            font=("Segoe UI", 13),
            text_color=TEXT
        )
        self.price_entry.pack(side="left", fill="both", expand=True, padx=(2, 8))
        self.price_entry.insert(0, str(self.room["price"]))

        self.error_label = ctk.CTkLabel(
            form,
            text="",
            height=20,
            font=("Segoe UI", 10),
            text_color="#DC2626",
            anchor="w"
        )
        self.error_label.pack(fill="x", padx=18)

        ctk.CTkFrame(
            form,
            height=1,
            fg_color="#E2E8F0",
            corner_radius=0
        ).pack(fill="x", padx=18, pady=(10, 16))

        ctk.CTkLabel(
            form,
            text="Estado operativo",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18)

        self.maintenance_var = ctk.BooleanVar(
            value=self.room["maintenance"]
        )
        self.maintenance_switch = ctk.CTkSwitch(
            form,
            text="En mantenimiento",
            variable=self.maintenance_var,
            onvalue=True,
            offvalue=False,
            font=("Segoe UI", 12),
            text_color="#334155",
            progress_color="#F59E0B",
            button_color="#FFFFFF",
            button_hover_color="#F8FAFC",
            cursor="hand2"
        )
        self.maintenance_switch.pack(anchor="w", padx=18, pady=(12, 4))

        ctk.CTkLabel(
            form,
            text="La ocupación se determina automáticamente por las reservas. "
                 "No se puede activar mantenimiento si hay reservas vigentes "
                 "o futuras.",
            font=("Segoe UI", 10),
            text_color="#64748B",
            justify="left",
            wraplength=370
        ).pack(anchor="w", padx=18, pady=(5, 18))

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=(0, 20))

        ctk.CTkButton(
            buttons,
            text="Cancelar",
            height=42,
            corner_radius=8,
            fg_color="#E2E8F0",
            text_color="#0F172A",
            hover_color="#CBD5E1",
            cursor="hand2",
            command=self.destroy
        ).pack(side="left", expand=True, padx=(0, 8))

        ctk.CTkButton(
            buttons,
            text="Guardar cambios",
            height=42,
            corner_radius=8,
            fg_color=PRIMARY,
            hover_color="#1D4ED8",
            cursor="hand2",
            command=self.save_changes
        ).pack(side="left", expand=True, padx=(8, 0))

    def save_changes(self):
        try:
            price = RoomValidator.parse_price(self.price_entry.get())
        except ValueError as error:
            self.error_label.configure(
                text=str(error)
            )
            self.price_entry.focus_set()
            return

        self.error_label.configure(text="")
        try:
            update_room_details(
                self.room["number"],
                price,
                self.maintenance_var.get()
            )
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror(
                title="No se pudo actualizar la habitación",
                message=str(error),
                parent=self
            )
            return

        if self.on_saved is not None:
            self.on_saved()
        self.destroy()
