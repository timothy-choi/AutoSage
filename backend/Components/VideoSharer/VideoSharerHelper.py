import os
import hashlib
from urllib.parse import urlencode
from datetime import datetime

SHARE_BASE_URL = ""

def generate_share_token(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist")

    stat = os.stat(file_path)
    key = f"{file_path}-{stat.st_size}-{stat.st_mtime}"
    token = hashlib.sha256(key.encode()).hexdigest()
    return token


def generate_shareable_link(file_path: str) -> str:
    token = generate_share_token(file_path)
    params = urlencode({"token": token, "file": os.path.basename(file_path)})
    return f"{SHARE_BASE_URL}?{params}"


def get_token_metadata(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist")

    stat = os.stat(file_path)
    return {
        "filename": os.path.basename(file_path),
        "size_bytes": stat.st_size,
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
    }


def validate_token(file_path: str, token: str) -> bool:
    try:
        expected = generate_share_token(file_path)
        return expected == token
    except FileNotFoundError:
        return False