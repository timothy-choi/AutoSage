import os
from typing import List
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

client = Client(account_sid, auth_token)

def send_bulk_whatsapp_messages(numbers: List[str], message: str) -> List[dict]:
    results = []
    for number in numbers:
        try:
            msg = client.messages.create(
                body=message,
                from_=from_whatsapp_number,
                to=number
            )
            results.append({"to": number, "sid": msg.sid, "status": "sent"})
        except Exception as e:
            results.append({"to": number, "error": str(e), "status": "failed"})
    return results