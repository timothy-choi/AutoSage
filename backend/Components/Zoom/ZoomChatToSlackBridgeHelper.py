import requests
import re

def extract_zoom_link(message):
    match = re.search(r"(https://[\w\.-]*zoom\.us/j/\d+)", message)
    return match.group(1) if match else None

def should_forward_message(sender_email, chat_type, message, allowed_domains, keywords, allow_group=False):
    if allowed_domains and not any(sender_email.endswith(domain) for domain in allowed_domains):
        return False, "unauthorized sender domain"

    if not allow_group and chat_type != "1on1":
        return False, "not a direct message"

    if keywords and not any(kw.lower() in message.lower() for kw in keywords):
        return False, "no keyword match"

    return True, None

def format_zoom_message_for_slack(sender_email, sender_name, message, timestamp, user_map=None):
    slack_user = user_map.get(sender_email, sender_name) if user_map else sender_name
    zoom_link = extract_zoom_link(message)

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*From:* {slack_user}\n*Time:* {timestamp}\n\n{message}"}
        }
    ]

    if zoom_link:
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Join Zoom Meeting"},
                    "url": zoom_link
                }
            ]
        })

    return {"text": f"Zoom Chat Message from {slack_user}", "blocks": blocks}

def forward_zoom_chat_to_slack(slack_webhook_url, sender_name, sender_email, message, timestamp, user_map=None):
    payload = format_zoom_message_for_slack(sender_email, sender_name, message, timestamp, user_map)
    response = requests.post(slack_webhook_url, json=payload)
    return {
        "status_code": response.status_code,
        "slack_response": response.text
    }