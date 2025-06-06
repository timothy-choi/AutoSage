from typing import List, Dict
from rapidfuzz import process

COMMAND_REGISTRY = {
    "messaging": [
        "send dm",
        "post update",
        "fetch user info",
        "notify channel",
        "schedule message"
    ],
    "threads": [
        "summarize thread",
        "reply to thread"
    ],
    "video": [
        "upload video",
        "compress video",
        "merge videos",
        "extract audio"
    ],
    "automation": [
        "start meeting",
        "create poll",
        "auto-respond"
    ]
}

ALL_COMMANDS = [cmd for group in COMMAND_REGISTRY.values() for cmd in group]

def autocomplete_command_fuzzy(partial: str, limit: int = 5) -> Dict[str, List[str]]:
    matches = process.extract(partial, ALL_COMMANDS, limit=limit, score_cutoff=30)
    matched_cmds = [match[0] for match in matches]

    grouped_results: Dict[str, List[str]] = {}
    for category, commands in COMMAND_REGISTRY.items():
        relevant = [cmd for cmd in commands if cmd in matched_cmds]
        if relevant:
            grouped_results[category] = relevant

    return grouped_results

autocomplete_command_fuzzy("vid")