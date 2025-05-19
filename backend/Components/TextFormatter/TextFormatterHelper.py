import textwrap
from typing import List

def capitalize_text(text: str) -> str:
    return text.capitalize()

def title_case_text(text: str) -> str:
    return text.title()

def upper_case_text(text: str) -> str:
    return text.upper()

def lower_case_text(text: str) -> str:
    return text.lower()

def reverse_text(text: str) -> str:
    return text[::-1]

def remove_whitespace(text: str) -> str:
    return " ".join(text.split())

def wrap_text(text: str, width: int = 80) -> str:
    return textwrap.fill(text, width=width)

def strip_punctuation(text: str) -> str:
    import string
    return text.translate(str.maketrans('', '', string.punctuation))

def count_words(text: str) -> int:
    return len(text.split())

def count_characters(text: str, include_spaces: bool = True) -> int:
    return len(text) if include_spaces else len(text.replace(" ", ""))