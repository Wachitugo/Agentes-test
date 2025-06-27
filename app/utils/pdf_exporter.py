from fpdf import FPDF
import os

def exportar_pdf(contenido: str, output_path: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    if os.path.isfile(font_path):
        pdf.add_font('DejaVu', '', font_path, uni=True)
        pdf.set_font('DejaVu', '', 12)
    else:
        print(f"Advertencia: fuente Unicode no encontrada en {font_path}, usando Arial")
        pdf.set_font('Arial', '', 12)
    for linea in contenido.split("\n"):
        pdf.multi_cell(0, 5, linea)
    pdf.output(output_path)