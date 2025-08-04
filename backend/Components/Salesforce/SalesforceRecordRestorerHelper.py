import requests

def restore_salesforce_record(instance_url: str, access_token: str, object_api_name: str, record_data: dict) -> dict:
    url = f"{instance_url}/services/data/v59.0/sobjects/{object_api_name}/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=record_data)
        response.raise_for_status()
        return {
            "success": True,
            "message": "Record restored by re-creating it.",
            "new_record_id": response.json().get("id")
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to restore record."
        }