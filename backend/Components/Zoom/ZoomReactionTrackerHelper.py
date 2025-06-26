import requests
from datetime import datetime

ALLOWED_REACTIONS = ["clap", "heart", "thumbs_up"]
REACTION_EMOJIS = {
    "clap": "👏",
    "heart": "❤️",
    "thumbs_up": "👍",
    "laugh": "😂",
    "wow": "😲"
}

def parse_reaction_event(payload: dict):
    obj = payload.get("payload", {}).get("object", {})
    participant = obj.get("participant", {})
    return {
        "meeting_id": obj.get("id"),
        "participant_user_id": participant.get("user_id"),
        "participant_name": participant.get("user_name"),
        "email": participant.get("email"),
        "reaction_type": participant.get("reaction_type"),
        "timestamp": participant.get("time")
    }

def is_reaction_allowed(reaction_type: str):
    return reaction_type in ALLOWED_REACTIONS

def is_email_domain_allowed(email: str, allowed_domains: list):
    return any(email.endswith("@" + domain.strip()) for domain in allowed_domains)

def format_human_time(iso_timestamp: str):
    try:
        return datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return iso_timestamp

def forward_reaction_to_webhook(reaction_data, webhook_url):
    try:
        response = requests.post(webhook_url, json=reaction_data)
        return {"status_code": response.status_code, "text": response.text}
    except Exception as e:
        return {"error": str(e)}
