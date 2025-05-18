import pyautogui
import os
from datetime import datetime
from typing import Optional, Tuple

def take_screenshot(filename: Optional[str] = None, region: Optional[Tuple[int, int, int, int]] = None) -> str:
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filename)
    return filename

def screenshot_to_bytes(region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
    from io import BytesIO
    buf = BytesIO()
    img = pyautogui.screenshot(region=region)
    img.save(buf, format='PNG')
    return buf.getvalue()

def save_screenshot_to_folder(folder: str = "screenshots") -> str:
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"screenshot_{timestamp}.png")
    pyautogui.screenshot().save(path)
    return path
