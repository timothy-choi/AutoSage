import requests

BASE_URL = "https://api.pinterest.com/v5"

def send_message(access_token: str, conversation_id: str, text: str):
    url = f"{BASE_URL}/conversations/{conversation_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to send message: {response.text}")
    return response.json()


def list_conversations(access_token: str, limit: int = 25):
    url = f"{BASE_URL}/conversations"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list conversations: {response.text}")
    return response.json()


def list_messages(access_token: str, conversation_id: str, limit: int = 25):
    url = f"{BASE_URL}/conversations/{conversation_id}/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list messages: {response.text}")
    return response.json()