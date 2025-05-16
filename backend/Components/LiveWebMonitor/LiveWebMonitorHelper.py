import time
import requests
import hashlib
from typing import Callable, Optional

def get_page_hash(url: str) -> Optional[str]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return hashlib.sha256(response.text.encode("utf-8")).hexdigest()
    except requests.RequestException:
        return None

def start_monitoring(
    url: str,
    on_change: Callable[[str, str], None],  # (url, new_content)
    check_interval: int = 60,
    run_once: bool = False,
    get_last_hash: Callable[[str], Optional[str]] = lambda _: None,
    get_current_hash: Callable[[str], Optional[str]] = lambda u: get_page_hash(u),
    save_hash: Callable[[str], None] = lambda h: None,
    get_last_content: Callable[[str], Optional[str]] = lambda _: None,
    get_current_content: Callable[[str], Optional[str]] = lambda u: fetch_page(u),
    save_content: Callable[[str], None] = lambda c: None,
):
    print(f"Monitoring {url} every {check_interval} seconds...")
    last_hash = get_last_hash(url)
    last_content = get_last_content(url)

    while True:
        new_hash = get_current_hash(url)
        new_content = get_current_content(url)

        if new_hash and new_hash != last_hash:
            if last_hash is not None:
                on_change(url, last_content, new_content)
            save_hash(new_hash)
            save_content(new_content)
            last_hash = new_hash
            last_content = new_content

        if run_once:
            break

        time.sleep(check_interval)

def fetch_page(url: str) -> Optional[str]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None
    
def content_has_changed(old: str, new: str) -> bool:
    return hashlib.sha256(old.encode()).hexdigest() != hashlib.sha256(new.encode()).hexdigest()