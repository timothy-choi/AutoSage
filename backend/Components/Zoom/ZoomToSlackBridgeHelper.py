import requests
from datetime import datetime

def fetch_zoom_meetings(user_id, jwt_token, meeting_type="upcoming"):
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    params = {"type": meeting_type, "page_size": 10}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Zoom meetings: {response.text}")
    
    return response.json().get("meetings", [])

def format_slack_message(meetings, meeting_type):
    if not meetings:
        return f":calendar: No {meeting_type} Zoom meetings found."

    blocks = [{
        "type": "section",
        "text": {"type": "mrkdwn", "text": f"*Zoom {meeting_type.title()} Meetings Sync*"}
    }]

    for m in meetings:
        start_time = m.get("start_time", "N/A")
        duration = m.get("duration", "N/A")
        topic = m.get("topic", "Untitled")
        join_url = m.get("join_url", "N/A")

        text = f"*{topic}*\n🕒 {start_time} | ⏱ {duration} mins\n🔗 <{join_url}|Join Link>"
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})
        blocks.append({"type": "divider"})

    return blocks

def post_to_slack(slack_webhook_url, blocks):
    payload = {"blocks": blocks}
    response = requests.post(slack_webhook_url, json=payload)
    return {
        "status": response.status_code,
        "success": response.status_code == 200,
        "detail": response.text if response.status_code != 200 else "Posted successfully"
    }

def sync_zoom_meetings_to_slack(user_id, jwt_token, slack_webhook_url, meeting_type="upcoming"):
    meetings = fetch_zoom_meetings(user_id, jwt_token, meeting_type)
    blocks = format_slack_message(meetings, meeting_type)
    return post_to_slack(slack_webhook_url, blocks)