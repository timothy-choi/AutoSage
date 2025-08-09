import requests

def trigger_process_builder(instance_url: str, access_token: str, object_name: str, record_id: str = None, fields: dict = None) -> dict:
    url = f"{instance_url}/services/data/v58.0/sobjects/{object_name}/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        if record_id:
            update_url = url + record_id
            response = requests.patch(update_url, headers=headers, json=fields)
            return {
                "success": response.status_code == 204,
                "operation": "update",
                "status_code": response.status_code
            }
        else:
            response = requests.post(url, headers=headers, json=fields)
            return {
                "success": response.status_code == 201,
                "operation": "create",
                "status_code": response.status_code,
                "id": response.json().get("id")
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to trigger Process Builder via record change"
        }