import pytesseract
from PIL import Image, ImageDraw
from typing import Optional, List, Dict

def extract_text_from_image(image_path: str, lang: str = 'eng') -> Optional[str]:
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return None

def extract_text_from_bytes(image_bytes: bytes, lang: str = 'eng') -> Optional[str]:
    try:
        from io import BytesIO
        img = Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return None

def get_text_data(image_path: str, lang: str = 'eng') -> List[Dict]:
    try:
        img = Image.open(image_path)
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        result = []
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                result.append({
                    'text': data['text'][i],
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'conf': data['conf'][i]
                })
        return result
    except Exception as e:
        print(f"OCR structured data error: {e}")
        return []

def get_image_with_boxes(image_path: str, lang: str = 'eng', save_path: Optional[str] = None) -> Optional[str]:
    try:
        img = Image.open(image_path)
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        draw = ImageDraw.Draw(img)
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
        if save_path:
            img.save(save_path)
            return save_path
        return None
    except Exception as e:
        print(f"OCR box draw error: {e}")
        return None

def get_words_with_confidence(image_path: str, lang: str = 'eng') -> List[Dict]:
    try:
        from pytesseract import Output
        img = Image.open(image_path)
        data = pytesseract.image_to_data(img, lang=lang, output_type=Output.DICT)
        return [
            {"text": text, "conf": conf}
            for text, conf in zip(data["text"], data["conf"])
            if text.strip()
        ]
    except Exception as e:
        print(f"OCR confidence error: {e}")
        return []
    
def extract_digits(image_path: str, lang: str = 'eng') -> str:
    try:
        img = Image.open(image_path)
        custom_config = r'--oem 3 --psm 11 outputbase digits'
        return pytesseract.image_to_string(img, lang=lang, config=custom_config).strip()
    except Exception as e:
        print(f"OCR digit extraction error: {e}")
        return ""

def detect_orientation(image_path: str) -> Optional[str]:
    try:
        result = pytesseract.image_to_osd(Image.open(image_path))
        return result.strip()
    except Exception as e:
        print(f"OCR orientation error: {e}")
        return None