import os
from typing import Dict, List
from datetime import datetime
from linkedin_api import Linkedin

LINKEDIN_USER = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASS = os.getenv("LINKEDIN_PASSWORD")

api = Linkedin(LINKEDIN_USER, LINKEDIN_PASS)

def send_message_to_connection(public_identifier: str, message: str) -> Dict:
    try:
        api.send_message(recipients=[public_identifier], message_body=message)
        return {
            "recipient": public_identifier,
            "status": "sent",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "recipient": public_identifier,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
    
def batch_send_messages(identifiers: List[str], message: str) -> List[Dict]:
    return [send_message_to_connection(pid, message) for pid in identifiers]


def check_connection_status(public_identifier: str) -> Dict:
    try:
        profile = api.get_profile(public_identifier)
        return {
            "identifier": public_identifier,
            "connection_degree": profile.get("entityUrn", "unknown")
        }
    except Exception as e:
        return {
            "identifier": public_identifier,
            "status": "error",
            "error": str(e)
        }

def get_recent_conversations(limit: int = 10) -> List[Dict]:
    try:
        convos = api.get_conversations()[:limit]
        return convos
    except Exception as e:
        return [{"status": "error", "error": str(e)}]