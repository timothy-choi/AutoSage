import qrcode
from typing import Optional
import io

def generate_qr_code(data: str, filename: Optional[str] = None, box_size: int = 10, border: int = 4) -> str:
    img = qrcode.make(data)

    if not filename:
        filename = "qr_code.png"

    img.save(filename)
    return filename

def generate_custom_qr_code(data: str, filename: Optional[str] = None, box_size: int = 10, border: int = 4) -> str:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    if not filename:
        filename = "qr_code.png"

    img.save(filename)
    return filename

def generate_qr_as_bytes(data: str, box_size: int = 10, border: int = 4) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def generate_qr_from_url(url: str, filename: Optional[str] = None) -> str:
    return generate_qr_code(url, filename)