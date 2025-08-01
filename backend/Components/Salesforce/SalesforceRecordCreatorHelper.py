import requests

def create_salesforce_record(instance_url: str, access_token: str, object_api_name: str, record_data: dict) -> dict:
    url = f"{instance_url}/services/data/v59.0/sobjects/{object_api_name}/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=record_data)
        if response.status_code == 201:
            data = response.json()
            return {
                "success": True,
                "id": data.get("id"),
                "object": object_api_name,
                "message": "Record created successfully."
            }
        else:
            return {
                "success": False,
                "message": "Failed to create record.",
                "status_code": response.status_code,
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Request exception occurred.",
            "error": str(e)
        }