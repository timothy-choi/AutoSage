from typing import List, Dict
import random
import os
import json

HASHTAG_BLOCK_FILE = os.getenv("HASHTAG_BLOCK_FILE", "hashtag_blocks.json")
EMOJI_FILE = os.getenv("EMOJI_FILE", "emojis.json")
CTA_FILE = os.getenv("CALL_TO_ACTION_FILE", "call_to_actions.json")
POST_TIMES_FILE = os.getenv("POST_TIMES_FILE", "post_times.json")

def load_json_file(path: str) -> List[str]:
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def generate_hashtag_block() -> str:
    blocks = load_json_file(HASHTAG_BLOCK_FILE)
    return " ".join(random.choice(blocks)) if blocks else ""

def emojify_text(text: str) -> str:
    emojis = load_json_file(EMOJI_FILE)
    return f"{random.choice(emojis)} {text} {random.choice(emojis)}" if emojis else text

def suggest_post_time() -> str:
    times = load_json_file(POST_TIMES_FILE)
    return random.choice(times) if times else "Anytime"

def summarize_text(text: str) -> str:
    if len(text) <= 120:
        return text
    return text[:117].rsplit(" ", 1)[0] + "..."

def generate_call_to_action() -> str:
    ctas = load_json_file(CTA_FILE)
    return random.choice(ctas) if ctas else "Share your thoughts."

def generate_caption(text: str) -> Dict:
    summary = summarize_text(text)
    return {
        "summary": summary,
        "caption": emojify_text(summary),
        "hashtags": generate_hashtag_block(),
        "suggested_time": suggest_post_time(),
        "call_to_action": generate_call_to_action()
    }