import os
from typing import List, Optional
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import textract # type: ignore
import shutil

def extract_text(doc_path: str) -> str:
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"File not found: {doc_path}")

    try:
        text = textract.process(doc_path).decode("utf-8")
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from DOC file: {e}")

def create_doc_from_text(text: str, output_path: str) -> str:
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to create DOC file: {e}")

def append_text_to_doc(doc_path: str, text: str) -> str:
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"File not found: {doc_path}")

    try:
        existing_text = textract.process(doc_path).decode("utf-8")
        combined_text = existing_text + "\n" + text
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(combined_text)
        return doc_path
    except Exception as e:
        raise RuntimeError(f"Failed to append text to DOC file: {e}")
    
def copy_doc(self, source_path: str, destination_path: str) -> str:
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File not found: {source_path}")
    try:
        shutil.copy(source_path, destination_path)
        return destination_path
    except Exception as e:
        raise RuntimeError(f"Failed to copy DOC file: {e}")

def rename_doc(self, original_path: str, new_path: str) -> str:
    if not os.path.exists(original_path):
        raise FileNotFoundError(f"File not found: {original_path}")
    try:
        os.rename(original_path, new_path)
        return new_path
    except Exception as e:
        raise RuntimeError(f"Failed to rename DOC file: {e}")

def delete_doc(self, doc_path: str) -> None:
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"File not found: {doc_path}")
    try:
        os.remove(doc_path)
    except Exception as e:
        raise RuntimeError(f"Failed to delete DOC file: {e}")