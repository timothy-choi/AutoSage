import os
import time
import base64
from typing import Optional


def generate_shareable_link(file_path: str, expiry_seconds: int = 3600) -> Optional[str]:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found")

        expiry = int(time.time()) + expiry_seconds
        data = f"{file_path}|{expiry}"
        encoded = base64.urlsafe_b64encode(data.encode()).decode()
        return f"http://localhost/share?token={encoded}"
    except Exception as e:
        print(f"Error generating shareable link: {e}")
        return None


def decode_shareable_link(token: str) -> Optional[str]:
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        file_path, expiry = decoded.split("|")
        if int(time.time()) > int(expiry):
            raise PermissionError("Link expired")
        return file_path
    except Exception as e:
        print(f"Error decoding link: {e}")
        return None
