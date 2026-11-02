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
    Image as PdfImage,
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
    receipt_number = f"R-{reservation['customer_dni']}-{timestamp[-6:]}"

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="BrandTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.white,
        alignment=TA_RIGHT
    ))
    styles.add(ParagraphStyle(
        name="BrandMeta",
        parent=styles["Normal"],
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#BFDBFE"),
        alignment=TA_RIGHT
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=2,
        spaceAfter=7
    ))
    styles.add(ParagraphStyle(
        name="FieldLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#64748B")
    ))
    styles.add(ParagraphStyle(
        name="FieldValue",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
    ))
    styles.add(ParagraphStyle(
        name="AmountLabel",
        parent=styles["Normal"],
        fontSize=9,
        leading=14,
        textColor=colors.HexColor("#475569")
    ))
    styles.add(ParagraphStyle(
        name="TotalLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        name="TotalValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.white,
        alignment=TA_RIGHT
    ))
    styles.add(ParagraphStyle(
        name="FooterText",
        parent=styles["Normal"],
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER
    ))

    def field(label, text):
        cell = Table(
            [
                [Paragraph(escape(label.upper()), styles["FieldLabel"])],
                [Paragraph(escape(str(text)), styles["FieldValue"])]
            ],
            colWidths=(76 * mm,)
        )
        cell.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ]))
        return cell

    def section(title, rows):
        heading = Paragraph(escape(title.upper()), styles["SectionTitle"])
        table = Table(
            rows,
            colWidths=(79 * mm, 79 * mm),
            hAlign="LEFT"
        )
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
        ]))
        return [heading, table]

    logo_path = project_root / "assets" / "logo.png"
    logo_image = PdfImage(str(logo_path))
    logo_scale = min(
        (55 * mm) / logo_image.imageWidth,
        (22 * mm) / logo_image.imageHeight
    )
    logo_image.drawWidth = logo_image.imageWidth * logo_scale
    logo_image.drawHeight = logo_image.imageHeight * logo_scale

    receipt_type = str(reservation.get("receipt_type") or "reserva").capitalize()
    status = reservation.get("display_status", "Confirmada")
    if status == "Cancelada":
        status_color = colors.HexColor("#C2410C")
    elif status == "Finalizada":
        status_color = colors.HexColor("#475569")
    else:
        status_color = colors.HexColor("#15803D")

    header_meta = [
        Paragraph("COMPROBANTE DE RESERVA", styles["BrandTitle"]),
        Spacer(1, 3 * mm),
        Paragraph(f"{receipt_type}  ·  {receipt_number}", styles["BrandMeta"]),
        Paragraph(
            datetime.now().strftime("EMITIDO %d/%m/%Y  ·  %H:%M"),
            styles["BrandMeta"]
        )
    ]
    header = Table(
        [[logo_image, header_meta]],
        colWidths=(67 * mm, 93 * mm),
        rowHeights=(31 * mm,)
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0B1F3A")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (0, 0), 5 * mm),
        ("RIGHTPADDING", (1, 0), (1, 0), 6 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
        ("LINEBELOW", (0, 0), (-1, -1), 2, colors.HexColor("#38BDF8"))
    ]))

    status_style = ParagraphStyle(
        "ReceiptStatus",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=status_color
    )
    status_banner = Table(
        [[
            Paragraph("ESTADO DE LA RESERVA", styles["FieldLabel"]),
            Paragraph(escape(str(status).upper()), status_style)
        ]],
        colWidths=(113 * mm, 47 * mm)
    )
    status_banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))

    customer_rows = [
        [
            field("Cliente", customer.get("customer_name", "—")),
            field("DNI", customer.get("customer_dni", reservation["customer_dni"]))
        ],
        [
            field("Teléfono", customer.get("customer_phone", "—"))
        ]
    ]
    stay_rows = [
        [
            field("Check-in", reservation["check_in"]),
            field("Check-out", reservation["check_out"])
        ],
        [
            field("Duración", f"{reservation['nights']} noches"),
            field("Huéspedes", reservation["guest_count"])
        ]
    ]
    room_rows = [
        [
            field("Habitación", reservation["room_number"]),
            field("Tipo", reservation["room_type"])
        ],
        [
            field("Método de pago", str(reservation.get("payment_method") or "—").capitalize()),
            field("Comprobante", receipt_type)
        ]
    ]

    amount_rows = [
        [Paragraph("Subtotal", styles["AmountLabel"]), Paragraph(f"S/ {reservation['subtotal']:.2f}", styles["AmountLabel"])],
        [Paragraph("IGV", styles["AmountLabel"]), Paragraph(f"S/ {reservation['igv']:.2f}", styles["AmountLabel"])]
    ]
    amount_table = Table(amount_rows, colWidths=(110 * mm, 50 * mm))
    amount_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2E8F0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    total_table = Table(
        [[
            Paragraph("TOTAL", styles["TotalLabel"]),
            Paragraph(f"S/ {reservation['total']:.2f}", styles["TotalValue"])
        ]],
        colWidths=(110 * mm, 50 * mm)
    )
    total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#123B6D")),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10)
    ]))

    document = SimpleDocTemplate(
        str(receipt_path),
        pagesize=A4,
        rightMargin=25 * mm,
        leftMargin=25 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm
    )
    document.build([
        header,
        Spacer(1, 7 * mm),
        status_banner,
        Spacer(1, 7 * mm),
        *section("Datos del cliente", customer_rows),
        Spacer(1, 5 * mm),
        *section("Detalle de la estadía", stay_rows),
        Spacer(1, 5 * mm),
        *section("Habitación y pago", room_rows),
        Spacer(1, 8 * mm),
        amount_table,
        Spacer(1, 3 * mm),
        total_table,
        Spacer(1, 12 * mm),
        Paragraph(
            "HOSTEL MELIMER  ·  Gracias por confiar en nosotros.",
            styles["FooterText"]
        ),
        Paragraph(
            f"Documento generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
            styles["FooterText"]
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
        try:
            os.startfile(str(receipt_path), "print")
        except OSError as error:
            if getattr(error, "winerror", None) != 1155:
                raise
            open_receipt(receipt_path)
            return False
    else:
        subprocess.Popen(["lp", str(receipt_path)])
    return True
