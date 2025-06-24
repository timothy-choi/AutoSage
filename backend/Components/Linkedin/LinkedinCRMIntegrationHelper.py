import requests

def format_crm_payload_from_linkedin(data: dict) -> dict:
    return {
        "name": data.get("name", "N/A"),
        "title": data.get("title", ""),
        "company": data.get("company", ""),
        "linkedin_url": data.get("linkedin_url", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "note": data.get("message", "")
    }


def send_lead_to_crm_webhook(webhook_url: str, payload: dict) -> dict:
    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        return {
            "status": "sent",
            "response_code": response.status_code,
            "sent_data": payload
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }