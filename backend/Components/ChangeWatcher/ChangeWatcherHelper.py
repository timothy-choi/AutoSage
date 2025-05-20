import os
import time
from typing import Callable, Optional


def watch_file_change(
    file_path: str,
    on_change: Callable[[str], None],
    check_interval: float = 1.0,
    run_once: bool = False,
) -> None:
    last_mtime = os.path.getmtime(file_path) if os.path.exists(file_path) else None

    while True:
        try:
            if os.path.exists(file_path):
                current_mtime = os.path.getmtime(file_path)
                if last_mtime is None or current_mtime != last_mtime:
                    on_change(file_path)
                    last_mtime = current_mtime
                    if run_once:
                        break
        except Exception as e:
            print(f"Error watching file: {e}")

        time.sleep(check_interval)


def watch_directory_change(
    directory_path: str,
    on_change: Callable[[str], None],
    check_interval: float = 2.0,
    run_once: bool = False,
) -> None:
    try:
        previous = {f: os.path.getmtime(os.path.join(directory_path, f)) for f in os.listdir(directory_path)}
    except FileNotFoundError:
        previous = {}

    while True:
        try:
            current = {f: os.path.getmtime(os.path.join(directory_path, f)) for f in os.listdir(directory_path)}
            changed = [f for f in current if f not in previous or current[f] != previous[f]]
            if changed:
                for f in changed:
                    on_change(os.path.join(directory_path, f))
                if run_once:
                    break
            previous = current
        except Exception as e:
            print(f"Error watching directory: {e}")

        time.sleep(check_interval)