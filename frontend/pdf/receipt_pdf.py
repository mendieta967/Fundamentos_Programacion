import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle
)


def generate_receipt(reservation, customer):

    project_root = Path(__file__).resolve().parents[1]
    receipts_dir = project_root / "data" / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    receipt_path = receipts_dir / f"reserva_{reservation['customer_dni']}_{timestamp}.pdf"

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReceiptTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="ReceiptSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name="ReceiptLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#334155")
    ))
    styles.add(ParagraphStyle(
        name="ReceiptValue",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#0F172A")
    ))
    styles.add(ParagraphStyle(
        name="ReceiptTotal",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_RIGHT
    ))

    def value(text):
        return Paragraph(escape(str(text)), styles["ReceiptValue"])

    details = [
        [Paragraph("Cliente", styles["ReceiptLabel"]), value(customer["customer_name"])],
        [Paragraph("DNI", styles["ReceiptLabel"]), value(customer["customer_dni"])],
        [Paragraph("Teléfono", styles["ReceiptLabel"]), value(customer["customer_phone"])],
        [Paragraph("Check-in", styles["ReceiptLabel"]), value(reservation["check_in"])],
        [Paragraph("Check-out", styles["ReceiptLabel"]), value(reservation["check_out"])],
        [Paragraph("Noches", styles["ReceiptLabel"]), value(reservation["nights"])],
        [Paragraph("Huéspedes", styles["ReceiptLabel"]), value(reservation["guest_count"])],
        [Paragraph("Habitación", styles["ReceiptLabel"]), value(reservation["room_number"])],
        [Paragraph("Tipo de habitación", styles["ReceiptLabel"]), value(reservation["room_type"])],
        [Paragraph("Método de pago", styles["ReceiptLabel"]), value(reservation["payment_method"].capitalize())],
        [Paragraph("Comprobante", styles["ReceiptLabel"]), value(reservation["receipt_type"].capitalize())]
    ]

    detail_table = Table(details, colWidths=(48 * mm, 112 * mm), hAlign="LEFT")
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E2E8F0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    totals = [
        [Paragraph("Subtotal", styles["ReceiptLabel"]), value(f"S/ {reservation['subtotal']:.2f}")],
        [Paragraph("IGV", styles["ReceiptLabel"]), value(f"S/ {reservation['igv']:.2f}")],
        [Paragraph("TOTAL", styles["ReceiptTotal"]), Paragraph(f"S/ {reservation['total']:.2f}", styles["ReceiptTotal"])]
    ]
    totals_table = Table(totals, colWidths=(48 * mm, 112 * mm), hAlign="LEFT")
    totals_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LINEABOVE", (0, 2), (-1, 2), 1, colors.HexColor("#CBD5E1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    document = SimpleDocTemplate(
        str(receipt_path),
        pagesize=A4,
        rightMargin=25 * mm,
        leftMargin=25 * mm,
        topMargin=25 * mm,
        bottomMargin=25 * mm
    )
    document.build([
        Paragraph("HOSTEL MELIMER", styles["ReceiptTitle"]),
        Paragraph(
            f"Comprobante de {escape(reservation['receipt_type'].lower())}",
            styles["ReceiptSubtitle"]
        ),
        Spacer(1, 12 * mm),
        detail_table,
        Spacer(1, 8 * mm),
        totals_table,
        Spacer(1, 14 * mm),
        Paragraph(
            "Gracias por elegir Hostel Melimer.",
            styles["ReceiptSubtitle"]
        )
    ])

    return receipt_path


def open_receipt(receipt_path):

    if sys.platform == "win32":
        os.startfile(str(receipt_path))
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(receipt_path)])
    else:
        subprocess.Popen(["xdg-open", str(receipt_path)])


def print_receipt(receipt_path):

    if sys.platform == "win32":
        os.startfile(str(receipt_path))
    else:
        subprocess.Popen(["lp", str(receipt_path)])
