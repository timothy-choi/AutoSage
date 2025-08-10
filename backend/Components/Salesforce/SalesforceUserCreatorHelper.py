import requests

def create_salesforce_user(instance_url: str, access_token: str, user_data: dict) -> dict:
    url = f"{instance_url}/services/data/v58.0/sobjects/User"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=user_data)
        if response.status_code == 201:
            return {"success": True, "user_id": response.json().get("id")}
        else:
            return {"success": False, "error": response.text}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}