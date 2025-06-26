import requests

def send_zoom_chat_message(access_token: str, to_jid: str, message: str, is_channel: bool = False):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = "https://api.zoom.us/v2/im/chat/messages"
    payload = {
        "message": message,
        "to_jid": to_jid,
        "account_id": "",  
        "is_markdown_support": True,
        "is_channel": is_channel
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in [200, 201, 204]:
        return {"status": "message_sent", "to_jid": to_jid, "is_channel": is_channel}
    return {"error": response.text, "status_code": response.status_code}