import os
from typing import List, Optional
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def extract_text(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def split_pdf(pdf_path: str, output_dir: str) -> List[str]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    output_files = []

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_path = os.path.join(output_dir, f"page_{i + 1}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
        output_files.append(output_path)

    return output_files

def merge_pdfs(pdf_paths: List[str], output_path: str) -> str:
    writer = PdfWriter()

    for path in pdf_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path

def create_pdf_from_text(
    text: str,
    output_path: str,
    font_name: str = "Helvetica",
    font_size: int = 12,
    margin: int = 40,
    line_spacing: int = 15
) -> str:
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont(font_name, font_size)

    width, height = letter
    y = height - margin

    for line in text.split('\n'):
        c.drawString(margin, y, line)
        y -= line_spacing
        if y < margin:
            c.showPage()
            c.setFont(font_name, font_size)
            y = height - margin

    c.save()
    return output_path

def encrypt_pdf(pdf_path: str, output_path: str, password: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)

    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path

def add_watermark(pdf_path: str, watermark_path: str, output_path: str) -> str:
    if not os.path.exists(pdf_path) or not os.path.exists(watermark_path):
        raise FileNotFoundError("PDF or watermark file not found")
    
    base_reader = PdfReader(pdf_path)
    watermark_reader = PdfReader(watermark_path)
    watermark_page = watermark_reader.pages[0]

    writer = PdfWriter()
    for page in base_reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path

def extract_pages(pdf_path: str, output_path: str, pages: List[int]) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for i in pages:
        if i < 1 or i > len(reader.pages):
            raise IndexError(f"Page number {i} is out of range")
        writer.add_page(reader.pages[i - 1])

    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path