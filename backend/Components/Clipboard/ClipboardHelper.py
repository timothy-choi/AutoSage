import pyperclip
import time
import os
import json
from typing import Optional

CLIPBOARD_DIR = "clipboard_history"
os.makedirs(CLIPBOARD_DIR, exist_ok=True)

def _get_user_history_path(user: str) -> str:
    return os.path.join(CLIPBOARD_DIR, f"clipboard_{user}.json")

def _load_history(user: str):
    path = _get_user_history_path(user)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def _save_history(user: str, history):
    path = _get_user_history_path(user)
    with open(path, "w") as f:
        json.dump(history, f)

def copy_to_clipboard(text: str, user: str) -> None:
    pyperclip.copy(text)
    history = _load_history(user)
    history.append({"timestamp": time.time(), "text": text})
    _save_history(user, history)

def paste_from_clipboard() -> str:
    return pyperclip.paste()

def clear_clipboard() -> None:
    pyperclip.copy("")

def is_clipboard_empty() -> bool:
    return paste_from_clipboard().strip() == ""

def get_clipboard_history(user: str, limit: int = 10) -> list:
    history = _load_history(user)
    return history[-limit:]

def has_clipboard_changed(last_value: str) -> bool:
    return paste_from_clipboard() != last_value

def wait_for_clipboard_change(last_value: str, timeout: float = 10.0) -> Optional[str]:
    start = time.time()
    while time.time() - start < timeout:
        current = paste_from_clipboard()
        if current != last_value:
            return current
        time.sleep(0.5)
    return None