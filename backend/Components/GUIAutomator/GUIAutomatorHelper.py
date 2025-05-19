import pyautogui
import time
from typing import Optional, Tuple


def click_at(x: int, y: int, delay: float = 0.0):
    time.sleep(delay)
    pyautogui.click(x, y)


def move_mouse_to(x: int, y: int, duration: float = 0.25):
    pyautogui.moveTo(x, y, duration=duration)


def type_text(text: str, interval: float = 0.05):
    pyautogui.write(text, interval=interval)


def press_key(key: str):
    pyautogui.press(key)


def hotkey(*keys: str):
    pyautogui.hotkey(*keys)


def screenshot_region(region: Optional[Tuple[int, int, int, int]] = None, filename: str = "screenshot.png") -> str:
    img = pyautogui.screenshot(region=region)
    img.save(filename)
    return filename


def locate_on_screen(image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if location:
        return location
    return None