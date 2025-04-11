from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_report(recognized_names, output_path="media/report.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Face Recognition Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = height - 120
    c.drawString(50, y, "Recognized students:")
    y -= 20

    if recognized_names:
        for name in recognized_names:
            c.drawString(70, y, f"- {name}")
            y -= 20
    else:
        c.drawString(70, y, "The faces are not recognized.")

    c.save()
    return output_path
