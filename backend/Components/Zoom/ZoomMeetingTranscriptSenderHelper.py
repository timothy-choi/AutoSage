import requests

from ZoomMeetingCreatorHelper import get_jwt_token

def fetch_meeting_recordings(api_key, api_secret, meeting_id):
    token = get_jwt_token(api_key, api_secret)
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"
    response = requests.get(url, headers=headers)
    return response.json() if response.ok else {"error": response.text}

def get_transcript_file_url(recordings_json):
    for file in recordings_json.get("recording_files", []):
        if file.get("file_type") == "TRANSCRIPT" and file.get("status") == "completed":
            return file.get("download_url")
    return None

def download_transcript(download_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(download_url, headers=headers)
    return response.text if response.ok else None

def send_transcript_to_webhook(transcript_text, webhook_url):
    response = requests.post(webhook_url, json={"transcript": transcript_text})
    return {
        "status_code": response.status_code,
        "response": response.text
    }