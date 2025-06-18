from datetime import datetime
from typing import List, Dict
import os
import json

async def generate_googlechat_daily_digest(messages: List[dict], date: str) -> str:
    summary_lines = [f"🗓️ *Google Chat Daily Digest for {date}*", ""]
    grouped = {}

    for msg in messages:
        sender = msg.get("sender", "Unknown")
        content = msg.get("content", "")
        grouped.setdefault(sender, []).append(content)

    for sender, entries in grouped.items():
        summary_lines.append(f"👤 {sender} ({len(entries)} messages):")
        for entry in entries:
            summary_lines.append(f"- {entry}")
        summary_lines.append("")

    digest = "\n".join(summary_lines)
    filename = f"digest_{date.replace('-', '')}.txt"
    filepath = os.path.join("digests", filename)
    os.makedirs("digests", exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(digest)

    return filepath

async def generate_digest_as_json(messages: List[Dict], date: str) -> str:
    grouped = {}
    for msg in messages:
        sender = msg.get("sender", "Unknown")
        grouped.setdefault(sender, []).append(msg.get("content", ""))

    digest_data = {
        "date": date,
        "digest": grouped
    }

    filename = f"digest_{date.replace('-', '')}.json"
    filepath = os.path.join("digests", filename)
    os.makedirs("digests", exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(digest_data, f, indent=2)

    return filepath

async def get_digest_summary_stats(messages: List[Dict]) -> Dict:
    stats = {}
    for msg in messages:
        sender = msg.get("sender", "Unknown")
        stats[sender] = stats.get(sender, 0) + 1

    total_messages = len(messages)
    top_contributor = max(stats, key=stats.get) if stats else None

    return {
        "total_messages": total_messages,
        "unique_senders": len(stats),
        "top_contributor": top_contributor,
        "messages_by_sender": stats
    }