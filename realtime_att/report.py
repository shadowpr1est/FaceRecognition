from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import datetime

def generate_pdf(names, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = os.path.join(output_dir, f"Отчёт_{date}.pdf")

    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(100, 800, f"Отчёт посещаемости от {datetime.datetime.now().strftime('%d.%m.%Y')}")

    y = 750
    for i, name in enumerate(names, 1):
        c.drawString(100, y, f"{i}. {name}")
        y -= 25
        if y < 50:
            c.showPage()
            y = 800

    c.save()
    return path
