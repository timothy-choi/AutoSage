import pyautogui
import time
from typing import Optional, List

def type_text(text: str, interval: float = 0.05):
    pyautogui.write(text, interval=interval)

def press_key(key: str):
    pyautogui.press(key)

def hotkey_combination(*keys: str):
    pyautogui.hotkey(*keys)

def hold_key(key: str, duration: float):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def press_keys_sequence(keys: List[str], interval: float = 0.1):
    for key in keys:
        pyautogui.press(key)
        time.sleep(interval)

def clear_line():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')

def repeat_key(key: str, count: int, interval: float = 0.05):
    for _ in range(count):
        pyautogui.press(key)
        time.sleep(interval)

def delay_typing(text: str, start_delay: float, interval: float = 0.05):
    time.sleep(start_delay)
    pyautogui.write(text, interval=interval)
