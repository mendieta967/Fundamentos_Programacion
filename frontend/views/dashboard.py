import customtkinter as ctk


class DashboardView(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(fg_color="transparent")

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            padx=30,
            pady=30,
            anchor="w"
        )