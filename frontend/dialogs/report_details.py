import customtkinter as ctk


class ReportDetailsDialog(ctk.CTkToplevel):

    def __init__(self, parent, title, report_data):
        master = parent.winfo_toplevel()
        super().__init__(master)

        self.title(title)
        self.geometry("900x650")
        self.minsize(720, 540)
        self.configure(fg_color="#F8FAFC")
        self.transient(master)
        self.grab_set()

        self._create_widgets(title, report_data)
        self._center_over_parent(master)
        self.bind("<Escape>", lambda _event: self.destroy())

    def _center_over_parent(self, parent):
        self.update_idletasks()
        parent.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    def _create_widgets(self, title, report_data):
        header = ctk.CTkFrame(
            self,
            fg_color="#0F172A",
            corner_radius=0,
            height=112
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="REPORTES  /  ANÁLISIS",
            font=("Segoe UI", 9, "bold"),
            text_color="#93C5FD"
        ).pack(anchor="w", padx=25, pady=(17, 2))

        ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI", 23, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", padx=25)

        ctk.CTkLabel(
            header,
            text="Datos del alojamiento · Reservas no canceladas",
            font=("Segoe UI", 10),
            text_color="#CBD5E1"
        ).pack(anchor="w", padx=25, pady=(2, 0))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=22, pady=(18, 12))

        self._create_metrics(body, report_data["metrics"])
        self._create_table(body, report_data["columns"], report_data["rows"])

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=22, pady=(0, 17))

        ctk.CTkLabel(
            footer,
            text=report_data["note"],
            font=("Segoe UI", 9),
            text_color="#64748B",
            anchor="w",
            justify="left",
            wraplength=650
        ).pack(side="left", fill="x", expand=True, padx=(0, 12))

        ctk.CTkButton(
            footer,
            text="Cerrar",
            width=100,
            height=36,
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            corner_radius=9,
            command=self.destroy
        ).pack(side="right")

    @staticmethod
    def _create_metrics(parent, metrics):
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", pady=(0, 15))

        for column in range(len(metrics)):
            section.grid_columnconfigure(column, weight=1, uniform="metric")

        for column, (label, value, detail) in enumerate(metrics):
            tile = ctk.CTkFrame(
                section,
                fg_color="#FFFFFF",
                corner_radius=12,
                border_width=1,
                border_color="#E2E8F0"
            )
            tile.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=(0, 7) if column < len(metrics) - 1 else (0, 0)
            )

            ctk.CTkLabel(
                tile,
                text=label,
                font=("Segoe UI", 8, "bold"),
                text_color="#64748B",
                anchor="w"
            ).pack(fill="x", padx=12, pady=(11, 3))

            ctk.CTkLabel(
                tile,
                text=value,
                font=("Segoe UI", 15, "bold"),
                text_color="#1D4ED8",
                anchor="w",
                justify="left",
                wraplength=220
            ).pack(fill="x", padx=12)

            ctk.CTkLabel(
                tile,
                text=detail,
                font=("Segoe UI", 9),
                text_color="#64748B",
                anchor="w",
                justify="left",
                wraplength=220
            ).pack(fill="x", padx=12, pady=(2, 10))

    @staticmethod
    def _create_table(parent, columns, rows):
        table = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )
        table.pack(fill="both", expand=True)
        table.grid_columnconfigure(0, weight=1)
        table.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(table, fg_color="#F1F5F9", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(
            tuple(range(len(columns))),
            weight=1,
            uniform="report-column"
        )

        for column, label in enumerate(columns):
            ctk.CTkLabel(
                header,
                text=label.upper(),
                font=("Segoe UI", 9, "bold"),
                text_color="#475569",
                anchor="w"
            ).grid(
                row=0,
                column=column,
                sticky="ew",
                padx=(15, 8),
                pady=12
            )

        content = ctk.CTkScrollableFrame(
            table,
            fg_color="#FFFFFF",
            corner_radius=0,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(
            tuple(range(len(columns))),
            weight=1,
            uniform="report-column"
        )

        if not rows:
            ctk.CTkLabel(
                content,
                text="No hay datos para mostrar en este informe.",
                font=("Segoe UI", 12),
                text_color="#64748B"
            ).grid(
                row=0,
                column=0,
                columnspan=len(columns),
                padx=20,
                pady=35
            )
            return

        for row_index, values in enumerate(rows):
            row_color = "#FFFFFF" if row_index % 2 == 0 else "#F8FAFC"
            row = ctk.CTkFrame(content, fg_color=row_color, corner_radius=0)
            row.grid(
                row=row_index,
                column=0,
                columnspan=len(columns),
                sticky="ew"
            )
            row.grid_columnconfigure(
                tuple(range(len(columns))),
                weight=1,
                uniform="report-column"
            )

            for column, value in enumerate(values):
                ctk.CTkLabel(
                    row,
                    text=str(value),
                    font=("Segoe UI", 10, "bold" if column == 0 else "normal"),
                    text_color="#0F172A" if column == 0 else "#475569",
                    anchor="w",
                    justify="left"
                ).grid(
                    row=0,
                    column=column,
                    sticky="ew",
                    padx=(15, 8),
                    pady=11
                )