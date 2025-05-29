import pytesseract
from PIL import Image, ImageFilter, ImageOps
import io

def solve_captcha_image(image_path: str) -> str:
    try:
        image = Image.open(image_path)
        preprocessed = preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed, config='--psm 8')
        return text.strip()
    except Exception as e:
        return f"[CaptchaSolver] Error: {e}"

def solve_captcha_bytes(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        preprocessed = preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed, config='--psm 8')
        return text.strip()
    except Exception as e:
        return f"[CaptchaSolver] Error: {e}"

def preprocess_image(image: Image.Image) -> Image.Image:
    image = image.convert("L")
    image = ImageOps.invert(image)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    image = image.point(lambda x: 0 if x < 140 else 255, '1')
    return image