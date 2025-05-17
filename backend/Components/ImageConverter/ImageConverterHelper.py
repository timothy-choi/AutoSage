from PIL import Image, ImageOps
import os
from typing import Optional, Tuple

def convert_image_format(src_path: str, dest_format: str, dest_path: Optional[str] = None) -> str:
    img = Image.open(src_path)
    dest_format = dest_format.upper()
    if not dest_path:
        base, _ = os.path.splitext(src_path)
        dest_path = f"{base}.{dest_format.lower()}"
    img.save(dest_path, format=dest_format)
    return dest_path

def resize_image(src_path: str, width: int, height: int, dest_path: Optional[str] = None) -> str:
    img = Image.open(src_path)
    resized_img = img.resize((width, height))
    if not dest_path:
        base, ext = os.path.splitext(src_path)
        dest_path = f"{base}_resized{ext}"
    resized_img.save(dest_path)
    return dest_path

def compress_image(src_path: str, quality: int = 75, dest_path: Optional[str] = None) -> str:
    img = Image.open(src_path)
    if not dest_path:
        base, ext = os.path.splitext(src_path)
        dest_path = f"{base}_compressed{ext}"
    img.save(dest_path, optimize=True, quality=quality)
    return dest_path

def crop_image(src_path: str, crop_box: Tuple[int, int, int, int], dest_path: Optional[str] = None) -> str:
    img = Image.open(src_path)
    cropped_img = img.crop(crop_box)
    if not dest_path:
        base, ext = os.path.splitext(src_path)
        dest_path = f"{base}_cropped{ext}"
    cropped_img.save(dest_path)
    return dest_path

def rotate_image(src_path: str, angle: float, dest_path: Optional[str] = None) -> str:
    img = Image.open(src_path)
    rotated_img = img.rotate(angle, expand=True)
    if not dest_path:
        base, ext = os.path.splitext(src_path)
        dest_path = f"{base}_rotated{ext}"
    rotated_img.save(dest_path)
    return dest_path

def convert_to_grayscale(src_path: str, dest_path: Optional[str] = None) -> str:
    img = Image.open(src_path)
    gray_img = ImageOps.grayscale(img)
    if not dest_path:
        base, ext = os.path.splitext(src_path)
        dest_path = f"{base}_gray{ext}"
    gray_img.save(dest_path)
    return dest_path

def create_thumbnail(src_path: str, size: Tuple[int, int] = (128, 128), dest_path: Optional[str] = None) -> str:
    img = Image.open(src_path)
    img.thumbnail(size)
    if not dest_path:
        base, ext = os.path.splitext(src_path)
        dest_path = f"{base}_thumbnail{ext}"
    img.save(dest_path)
    return dest_path