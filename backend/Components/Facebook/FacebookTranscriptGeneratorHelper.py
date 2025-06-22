from typing import List, Dict
from datetime import datetime

def format_timestamp(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts

def generate_transcript(posts: List[Dict], comments: List[Dict]) -> str:
    transcript_lines = []

    post_lookup = {p["id"]: p for p in posts}

    for post in posts:
        time_str = format_timestamp(post.get("created_time", ""))
        transcript_lines.append(f"\n🟦 POST by {post.get('from', {}).get('name', 'Unknown')} at {time_str}")
        transcript_lines.append(f"📝 {post.get('message', '[No message]')}\n")

        related_comments = [c for c in comments if c.get("post_id") == post["id"]]
        for comment in related_comments:
            c_time = format_timestamp(comment.get("created_time", ""))
            c_user = comment.get("from", {}).get("name", "Unknown")
            c_text = comment.get("message", "[No comment]")
            transcript_lines.append(f"💬 {c_user} at {c_time}: {c_text}")

    return "\n".join(transcript_lines).strip()