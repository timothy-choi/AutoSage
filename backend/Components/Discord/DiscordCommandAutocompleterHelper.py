from rapidfuzz import process
from typing import List, Dict

COMMAND_CATALOG = {
    "threads": [
        "archive thread",
        "reply to thread",
        "summarize thread"
    ],
    "messages": [
        "send message",
        "send markdown",
        "send embed",
        "send DM",
        "mention users"
    ],
    "media": [
        "upload video",
        "convert video",
        "compress image",
        "add watermark"
    ],
    "automation": [
        "create poll",
        "auto-reply",
        "schedule message",
        "extract keywords"
    ],
    "user actions": [
        "fetch user info",
        "ban user",
        "assign role",
        "list members"
    ]
}

ALL_COMMANDS = [cmd for group in COMMAND_CATALOG.values() for cmd in group]

def autocomplete_command(input_text: str, limit: int = 5, threshold: int = 30) -> Dict[str, List[str]]:
    matches = process.extract(input_text, ALL_COMMANDS, limit=limit, score_cutoff=threshold)
    match_set = [match[0] for match in matches]

    result = {}
    for category, cmds in COMMAND_CATALOG.items():
        filtered = [cmd for cmd in cmds if cmd in match_set]
        if filtered:
            result[category] = filtered

    return result