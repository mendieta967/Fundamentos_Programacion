from textwrap import fill

import customtkinter as ctk


ALERT_STYLES = {
    "error": {
        "label": "ERROR",
        "accent": "#B91C1C",
        "hover": "#991B1B",
        "soft": "#FEE2E2",
        "text": "#7F1D1D",
        "symbol": "×"
    },
    "warning": {
        "label": "ATENCIÓN",
        "accent": "#B45309",
        "hover": "#92400E",
        "soft": "#FEF3C7",
        "text": "#78350F",
        "symbol": "!"
    },
    "info": {
        "label": "INFORMACIÓN",
        "accent": "#1D4ED8",
        "hover": "#1E40AF",
        "soft": "#DBEAFE",
        "text": "#1E3A8A",
        "symbol": "i"
    }
}


class AlertDialog(ctk.CTkToplevel):

    def __init__(self, parent, title, message, severity):
        master = parent.winfo_toplevel() if parent is not None else None
        super().__init__(master)

        self.style = ALERT_STYLES[severity]
        self.title(title)
        self.resizable(False, False)
        self.configure(fg_color="#F8FAFC")

        if master is not None:
            self.transient(master)
        self._create_widgets(title, message)
        self._center_over_parent(master, message)
        self.grab_set()
        self.bind("<Return>", lambda _event: self.destroy())
        self.bind("<Escape>", lambda _event: self.destroy())

    def _center_over_parent(self, parent, message):
        self.update_idletasks()
        width = 500
        lines = len(fill(str(message), width=58).splitlines())
        height = min(390, max(245, 204 + lines * 23))

        if parent is not None:
            parent.update_idletasks()
            x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
            y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        else:
            x = (self.winfo_screenwidth() - width) // 2
            y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")

    def _create_widgets(self, title, message):
        header = ctk.CTkFrame(
            self,
            fg_color=self.style["accent"],
            corner_radius=0,
            height=68
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=self.style["symbol"],
            width=38,
            height=38,
            fg_color="#FFFFFF",
            text_color=self.style["accent"],
            corner_radius=19,
            font=("Segoe UI", 22, "bold")
        ).pack(side="left", padx=(20, 12), pady=15)

        ctk.CTkLabel(
            header,
            text=self.style["label"],
            font=("Segoe UI", 14, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left")

        alert_card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color=self.style["soft"]
        )
        alert_card.pack(fill="both", expand=True, padx=22, pady=(18, 12))

        ctk.CTkLabel(
            alert_card,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=self.style["text"],
            anchor="w",
            wraplength=430
        ).pack(fill="x", padx=16, pady=(15, 5))

        ctk.CTkLabel(
            alert_card,
            text=fill(str(message), width=58),
            width=430,
            font=("Segoe UI", 12),
            text_color="#334155",
            justify="left",
            anchor="w",
            wraplength=430
        ).pack(fill="both", expand=True, padx=16, pady=(0, 14))

        ctk.CTkButton(
            self,
            text="Entendido",
            width=128,
            height=40,
            corner_radius=8,
            fg_color=self.style["accent"],
            hover_color=self.style["hover"],
            text_color="white",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=self.destroy
        ).pack(anchor="e", padx=22, pady=(0, 18))

    def show(self):
        self.wait_window()
        return "ok"


class MessageBox:

    @staticmethod
    def showerror(title, message, parent=None):
        return AlertDialog(parent, title, message, "error").show()

    @staticmethod
    def showwarning(title, message, parent=None):
        return AlertDialog(parent, title, message, "warning").show()

    @staticmethod
    def showinfo(title, message, parent=None):
        return AlertDialog(parent, title, message, "info").show()


messagebox = MessageBox()
