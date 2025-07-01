import requests

def get_zoom_user_presence(user_id: str, jwt_token: str) -> dict:
    url = f"https://api.zoom.us/v2/users/{user_id}/presence_status"
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {
            "user_id": user_id,
            "error": response.text,
            "status": "Unknown"
        }

    data = response.json()
    return {
        "user_id": user_id,
        "presence_status": data.get("presence_status", "Unknown"),
        "status_message": data.get("status", "")
    }

def get_multiple_user_presences(user_ids: list, jwt_token: str) -> list:
    results = []
    for uid in user_ids:
        result = get_zoom_user_presence(uid, jwt_token)
        results.append(result)
    return results