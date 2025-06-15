import re
from typing import List

blocked_keywords: List[str] = []
allowed_keywords: List[str] = []

def set_blocked_keywords(keywords: List[str]):
    global blocked_keywords
    blocked_keywords = keywords

def set_allowed_keywords(keywords: List[str]):
    global allowed_keywords
    allowed_keywords = keywords

def scan_message(message: str) -> dict:
    message_lower = message.lower()
    violations = [kw for kw in blocked_keywords if re.search(rf"\\b{re.escape(kw)}\\b", message_lower)]
    safe_hits = [kw for kw in allowed_keywords if re.search(rf"\\b{re.escape(kw)}\\b", message_lower)]

    return {
        "blocked_hits": violations,
        "allowed_hits": safe_hits,
        "status": "flagged" if violations else "ok"
    }