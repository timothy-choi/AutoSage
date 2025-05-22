import time
import pyautogui
import json
import os
from typing import List, Dict, Union, Optional

MacroStep = Dict[str, Union[str, int, float, List[str]]]

MACRO_DIR = "saved_macros"
os.makedirs(MACRO_DIR, exist_ok=True)

def execute_macro(steps: List[MacroStep]) -> None:
    for step in steps:
        action = step.get("action")
        try:
            if action == "click":
                x = step.get("x")
                y = step.get("y")
                delay = step.get("delay", 0.0)
                if x is not None and y is not None:
                    time.sleep(delay)
                    pyautogui.click(x, y)

            elif action == "doubleclick":
                x = step.get("x")
                y = step.get("y")
                delay = step.get("delay", 0.0)
                if x is not None and y is not None:
                    time.sleep(delay)
                    pyautogui.doubleClick(x, y)

            elif action == "move":
                x = step.get("x")
                y = step.get("y")
                duration = step.get("duration", 0.25)
                if x is not None and y is not None:
                    pyautogui.moveTo(x, y, duration=duration)

            elif action == "drag":
                x = step.get("x")
                y = step.get("y")
                duration = step.get("duration", 0.5)
                if x is not None and y is not None:
                    pyautogui.dragTo(x, y, duration=duration)

            elif action == "type":
                text = step.get("text", "")
                interval = step.get("interval", 0.05)
                pyautogui.write(str(text), interval=interval)

            elif action == "key":
                key = step.get("key")
                if key:
                    pyautogui.press(key)

            elif action == "hotkey":
                keys = step.get("keys")
                if isinstance(keys, list):
                    pyautogui.hotkey(*keys)

            elif action == "scroll":
                amount = step.get("amount", 0)
                pyautogui.scroll(int(amount))

            elif action == "wait":
                duration = step.get("duration", 1.0)
                time.sleep(duration)

        except Exception as e:
            print(f"Macro step failed: {step} - Error: {e}")

def validate_macro(steps: List[MacroStep]) -> bool:
    """Check if the macro steps are syntactically valid."""
    allowed_actions = {"click", "move", "doubleclick", "drag", "type", "key", "hotkey", "scroll", "wait"}
    for step in steps:
        if "action" not in step or step["action"] not in allowed_actions:
            return False
    return True

def summarize_macro(steps: List[MacroStep]) -> List[str]:
    """Return a short human-readable summary of macro steps."""
    summary = []
    for i, step in enumerate(steps):
        desc = f"Step {i+1}: {step.get('action')}"
        if step.get("action") in {"click", "move", "doubleclick", "drag"}:
            desc += f" at ({step.get('x')}, {step.get('y')})"
        elif step.get("action") == "type":
            desc += f" '{step.get('text')}'"
        elif step.get("action") == "key":
            desc += f" key '{step.get('key')}'"
        elif step.get("action") == "hotkey":
            desc += f" keys {step.get('keys')}"
        elif step.get("action") == "scroll":
            desc += f" by {step.get('amount')} units"
        elif step.get("action") == "wait":
            desc += f" for {step.get('duration')}s"
        summary.append(desc)
    return summary

def save_macro(name: str, steps: List[MacroStep]) -> None:
    with open(os.path.join(MACRO_DIR, f"{name}.json"), "w") as f:
        json.dump(steps, f)

def load_macro(name: str) -> Optional[List[MacroStep]]:
    path = os.path.join(MACRO_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def list_macros() -> List[str]:
    return [f[:-5] for f in os.listdir(MACRO_DIR) if f.endswith(".json")]

def run_saved_macro(name: str) -> None:
    steps = load_macro(name)
    if steps and validate_macro(steps):
        execute_macro(steps)