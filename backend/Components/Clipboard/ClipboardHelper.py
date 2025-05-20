import pyperclip
from typing import Optional
import time

_clipboard_history = []


def copy_to_clipboard(text: str) -> None:
    pyperclip.copy(text)
    _clipboard_history.append((time.time(), text))


def paste_from_clipboard() -> str:
    return pyperclip.paste()


def clear_clipboard() -> None:
    pyperclip.copy("")


def is_clipboard_empty() -> bool:
    return paste_from_clipboard().strip() == ""


def get_clipboard_history(limit: int = 10) -> list:
    return _clipboard_history[-limit:]


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