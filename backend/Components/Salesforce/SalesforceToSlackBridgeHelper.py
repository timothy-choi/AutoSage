import requests

def send_salesforce_event_to_slack(slack_webhook_url: str, event_data: dict) -> dict:
    slack_message = {
        "text": "*New Salesforce Event Triggered!*",
        "attachments": [
            {
                "color": "#36a64f",
                "fields": [
                    {"title": "Event Type", "value": event_data.get("type", "Unknown"), "short": True},
                    {"title": "Object", "value": event_data.get("object", "N/A"), "short": True},
                    {"title": "Record ID", "value": event_data.get("record_id", "N/A"), "short": False},
                    {"title": "Details", "value": event_data.get("details", "No additional info."), "short": False},
                ]
            }
        ]
    }

    try:
        response = requests.post(slack_webhook_url, json=slack_message)
        if response.status_code == 200:
            return {"success": True, "message": "Message sent to Slack."}
        else:
            return {"success": False, "error": response.text}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}