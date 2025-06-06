import requests

def fetch_slack_user_info(token: str, user_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "user": user_id
    }

    response = requests.get("https://slack.com/api/users.info", headers=headers, params=params)
    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(data.get("error", "Failed to fetch user info"))

    user = data["user"]
    return {
        "id": user.get("id"),
        "name": user.get("real_name"),
        "display_name": user.get("profile", {}).get("display_name"),
        "email": user.get("profile", {}).get("email"),
        "status_text": user.get("profile", {}).get("status_text"),
        "status_emoji": user.get("profile", {}).get("status_emoji"),
        "image": user.get("profile", {}).get("image_192"),
        "timezone": user.get("tz")
    }