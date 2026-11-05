import customtkinter as ctk

from frontend.dialogs.alerts import messagebox
from frontend.dialogs.report_details import ReportDetailsDialog
from modules.reports.report_data import get_report_data


class ReportsView(ctk.CTkFrame):

    REPORTS = (
        (
            "today",
            "01",
            "Reservas del día",
            "Revisá los ingresos programados para hoy.",
            "OPERACIÓN",
            "#2563EB",
            "#EFF6FF"
        ),
        (
            "frequent_customers",
            "02",
            "Clientes frecuentes",
            "Conocé quiénes reservan con mayor frecuencia.",
            "CLIENTES",
            "#7C3AED",
            "#F5F3FF"
        ),
        (
            "most_reserved_room",
            "03",
            "Habitación más reservada",
            "Descubrí qué habitaciones tienen mayor demanda.",
            "HABITACIONES",
            "#0891B2",
            "#ECFEFF"
        ),
        (
            "room_income",
            "04",
            "Ingresos por habitación",
            "Compará el total facturado por cada habitación.",
            "RENDIMIENTO",
            "#059669",
            "#ECFDF5"
        ),
        (
            "total_income",
            "05",
            "Ingresos totales",
            "Consultá el total facturado y el promedio por reserva.",
            "FINANZAS",
            "#D97706",
            "#FFFBEB"
        ),
        (
            "occupancy",
            "06",
            "Ocupación del hotel",
            "Revisá habitaciones ocupadas, disponibles y en mantenimiento.",
            "EN TIEMPO REAL",
            "#DB2777",
            "#FDF2F8"
        )
    )

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#F8FAFC")
        self._create_layout()

    def _create_layout(self):
        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        content.pack(fill="both", expand=True, padx=34, pady=(25, 20))

        self._create_heading(content)
        self._create_intro_card(content)
        self._create_reports_section(content)
        self._create_note(content)

    @staticmethod
    def _create_heading(parent):
        heading = ctk.CTkFrame(parent, fg_color="transparent")
        heading.pack(fill="x", pady=(0, 20))

        title_block = ctk.CTkFrame(heading, fg_color="transparent")
        title_block.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_block,
            text="Centro de reportes",
            font=("Segoe UI", 27, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_block,
            text="Indicadores claros para tomar mejores decisiones.",
            font=("Segoe UI", 12),
            text_color="#64748B"
        ).pack(anchor="w", pady=(3, 0))

        ctk.CTkLabel(
            heading,
            text="●  DATOS ACTUALIZADOS",
            fg_color="#ECFDF5",
            text_color="#047857",
            corner_radius=8,
            font=("Segoe UI", 9, "bold"),
            padx=11,
            pady=7
        ).pack(side="right", pady=(7, 0))

    @staticmethod
    def _create_intro_card(parent):
        intro = ctk.CTkFrame(
            parent,
            fg_color="#0F172A",
            corner_radius=16,
            height=122
        )
        intro.pack(fill="x", pady=(0, 24))
        intro.pack_propagate(False)

        accent = ctk.CTkFrame(
            intro,
            fg_color="#3B82F6",
            width=4,
            corner_radius=2
        )
        accent.pack(side="left", fill="y", padx=(18, 15), pady=19)

        text = ctk.CTkFrame(intro, fg_color="transparent")
        text.pack(side="left", fill="both", expand=True, pady=22, padx=(0, 16))

        ctk.CTkLabel(
            text,
            text="Una lectura inteligente del negocio",
            font=("Segoe UI", 16, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text,
            text="Explorá reservas, clientes, habitaciones, ingresos y ocupación.",
            font=("Segoe UI", 11),
            text_color="#CBD5E1"
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            intro,
            text="ANÁLISIS  /  06 REPORTES",
            fg_color="#1E293B",
            text_color="#BFDBFE",
            corner_radius=8,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8
        ).pack(side="right", padx=20)

    def _create_reports_section(self, parent):
        section_header = ctk.CTkFrame(parent, fg_color="transparent")
        section_header.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            section_header,
            text="Reportes disponibles",
            font=("Segoe UI", 16, "bold"),
            text_color="#0F172A"
        ).pack(side="left")

        ctk.CTkLabel(
            section_header,
            text="SELECCIONÁ UN INFORME PARA EXPLORAR",
            font=("Segoe UI", 9, "bold"),
            text_color="#94A3B8"
        ).pack(side="right", pady=(3, 0))

        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1), weight=1, uniform="report")

        for index, report in enumerate(self.REPORTS):
            row, column = divmod(index, 2)
            self._create_report_card(grid, report, row, column)

    def _create_report_card(self, parent, report, row, column):
        key, number, title, description, category, accent, tint = report
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0",
            height=158
        )
        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=(0, 8) if column == 0 else (8, 0),
            pady=(0, 14)
        )
        card.grid_propagate(False)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=13)

        top = ctk.CTkFrame(content, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text=number,
            width=34,
            height=31,
            fg_color=tint,
            text_color=accent,
            corner_radius=9,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=category,
            fg_color=tint,
            text_color=accent,
            corner_radius=7,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=5
        ).pack(side="right")

        ctk.CTkLabel(
            content,
            text=title,
            font=("Segoe UI", 13, "bold"),
            text_color="#0F172A",
            anchor="w"
        ).pack(fill="x", pady=(9, 3))

        ctk.CTkLabel(
            content,
            text=description,
            font=("Segoe UI", 10),
            text_color="#64748B",
            anchor="w",
            justify="left",
            wraplength=360
        ).pack(fill="x")

        ctk.CTkButton(
            content,
            text="Abrir informe  →",
            height=28,
            fg_color="transparent",
            hover_color=tint,
            text_color=accent,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            cursor="hand2",
            command=lambda report_key=key, report_title=title: self._open_report(
                report_key,
                report_title
            )
        ).pack(anchor="w", pady=(4, 0))

    @staticmethod
    def _create_note(parent):
        note = ctk.CTkFrame(parent, fg_color="#F1F5F9", corner_radius=9)
        note.pack(fill="x", pady=(1, 2))

        ctk.CTkLabel(
            note,
            text="CRITERIO DE DATOS",
            font=("Segoe UI", 9, "bold"),
            text_color="#475569"
        ).pack(side="left", padx=(13, 8), pady=10)

        ctk.CTkLabel(
            note,
            text="Los reportes históricos excluyen reservas canceladas.",
            font=("Segoe UI", 10),
            text_color="#64748B"
        ).pack(side="left", pady=10)

    def _open_report(self, report_key, title):
        try:
            data = get_report_data(report_key)
        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                "No se pudo generar el informe",
                str(error),
                parent=self
            )
            return

        ReportDetailsDialog(self, title, data)
