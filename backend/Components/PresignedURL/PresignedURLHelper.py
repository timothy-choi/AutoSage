import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import Optional

SECRET_KEY = b'super-secret-key'  # Keep this safe and private!


def generate_custom_presigned_url(base_url: str, file_path: str, expires_in: int = 3600) -> str:
    expiration = int(time.time()) + expires_in
    payload = f"{file_path}:{expiration}"
    signature = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()

    query = urllib.parse.urlencode({
        "file": file_path,
        "expires": expiration,
        "signature": signature
    })
    return f"{base_url}?{query}"


def validate_presigned_url(file: str, expires: str, signature: str) -> bool:
    try:
        if int(expires) < time.time():
            return False
        payload = f"{file}:{expires}"
        expected_sig = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, signature)
    except Exception:
        return False