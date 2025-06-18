from typing import Dict
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

client = Client(account_sid, auth_token)

template_store: Dict[str, str] = {}

def create_template(template_name: str, content: str) -> str:
    if template_name in template_store:
        raise ValueError("Template name already exists.")
    template_store[template_name] = content
    return "created"

def update_template(template_name: str, content: str) -> str:
    if template_name not in template_store:
        raise ValueError("Template not found.")
    template_store[template_name] = content
    return "updated"

def get_template(template_name: str) -> str:
    if template_name not in template_store:
        raise ValueError("Template not found.")
    return template_store[template_name]

def delete_template(template_name: str) -> str:
    if template_name in template_store:
        del template_store[template_name]
        return "deleted"
    raise ValueError("Template not found.")

def list_templates() -> Dict[str, str]:
    return template_store

def send_template_message(to_number: str, template_name: str, variables: Dict[str, str]) -> str:
    if template_name not in template_store:
        raise ValueError("Template not found.")
    
    content = template_store[template_name]
    for key, value in variables.items():
        content = content.replace(f"{{{{{key}}}}}", value)

    msg = client.messages.create(
        body=content,
        from_=from_whatsapp_number,
        to=to_number
    )
    return msg.sid