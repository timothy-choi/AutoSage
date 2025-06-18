from datetime import datetime
from typing import List
import json
import os
import csv

async def generate_googlechat_transcript(messages: List[dict], thread_id: str) -> str:
    lines = []
    for msg in messages:
        timestamp = msg.get("timestamp", datetime.utcnow().isoformat())
        sender = msg.get("sender", "Unknown")
        content = msg.get("content", "")
        lines.append(f"[{timestamp}] {sender}: {content}")

    transcript = "\n".join(lines)
    filename = f"transcript_{thread_id}.txt"
    filepath = os.path.join("transcripts", filename)
    os.makedirs("transcripts", exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(transcript)

    return filepath

async def generate_transcript_as_json(messages: List[dict], thread_id: str) -> str:
    filename = f"transcript_{thread_id}.json"
    filepath = os.path.join("transcripts", filename)
    os.makedirs("transcripts", exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)

    return filepath

async def generate_transcript_as_csv(messages: List[dict], thread_id: str) -> str:
    filename = f"transcript_{thread_id}.csv"
    filepath = os.path.join("transcripts", filename)
    os.makedirs("transcripts", exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "sender", "content"])
        writer.writeheader()
        for msg in messages:
            writer.writerow({
                "timestamp": msg.get("timestamp", ""),
                "sender": msg.get("sender", ""),
                "content": msg.get("content", "")
            })

    return filepath