import requests
from ZoomMeetingCreatorHelper import get_jwt_token

def create_zoom_poll(api_key, api_secret, meeting_id, title, questions):
    token = get_jwt_token(api_key, api_secret)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    poll_payload = {
        "title": title,
        "questions": []
    }

    for q in questions:
        poll_payload["questions"].append({
            "name": q["name"],
            "type": "multiple" if q.get("type") == "multiple" else "single",
            "answers": q.get("answers", [])
        })

    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/polls"
    response = requests.post(url, headers=headers, json=poll_payload)

    return response.json() if response.ok else {"error": response.text, "status_code": response.status_code}