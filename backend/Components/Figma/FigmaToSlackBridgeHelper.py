import requests

def send_figma_update_to_slack(slack_webhook_url: str, message: str, attachments: list = None) -> dict:
    payload = {
        "text": message
    }

    if attachments:
        payload["attachments"] = attachments

    response = requests.post(slack_webhook_url, json=payload)

    if response.status_code == 200:
        return {"status": "success", "message": "Sent update to Slack"}
    else:
        return {
            "status": "error",
            "message": f"Failed to send to Slack: {response.status_code}",
            "details": response.text
        }

def format_figma_comment_message(file_name: str, commenter: str, comment_text: str, file_url: str) -> str:
    return (
        f"*New Figma Comment* on `{file_name}`\n"
        f"👤 *{commenter}*: {comment_text}\n"
        f"🔗 [Open in Figma]({file_url})"
    )

def format_figma_activity_summary(file_name: str, last_modified: str, file_url: str) -> str:
    return (
        f"*Figma File Updated*: `{file_name}`\n"
        f"🕒 Last Modified: {last_modified}\n"
        f"🔗 [Open File]({file_url})"
    )