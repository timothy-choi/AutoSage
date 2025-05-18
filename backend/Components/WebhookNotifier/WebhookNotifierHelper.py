import requests
import time
from typing import Dict, Optional, Any

MAX_RETRIES = 3
RETRY_DELAY = 2  

def send_webhook(webhook_url: str, payload: Dict, headers: Optional[Dict[str, str]] = None, timeout: int = 5) -> Dict:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(webhook_url, json=payload, headers=headers or {}, timeout=timeout)
            return {
                "status_code": response.status_code,
                "response": response.text,
                "attempt": attempt
            }
        except requests.RequestException as e:
            if attempt == MAX_RETRIES:
                return {
                    "status_code": 0,
                    "error": str(e),
                    "attempt": attempt
                }
            time.sleep(RETRY_DELAY)

def send_text_webhook(webhook_url: str, message: str, headers: Optional[Dict[str, str]] = None, timeout: int = 5) -> Dict:
    payload = {"text": message}
    return send_webhook(webhook_url, payload, headers, timeout)

def send_form_webhook(webhook_url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None, timeout: int = 5) -> Dict:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(webhook_url, data=data, headers=headers or {}, timeout=timeout)
            return {
                "status_code": response.status_code,
                "response": response.text,
                "attempt": attempt
            }
        except requests.RequestException as e:
            if attempt == MAX_RETRIES:
                return {
                    "status_code": 0,
                    "error": str(e),
                    "attempt": attempt
                }
            time.sleep(RETRY_DELAY)

def send_webhook_with_auth(webhook_url: str, payload: Dict, token: str, timeout: int = 5) -> Dict:
    headers = {"Authorization": f"Bearer {token}"}
    return send_webhook(webhook_url, payload, headers, timeout)