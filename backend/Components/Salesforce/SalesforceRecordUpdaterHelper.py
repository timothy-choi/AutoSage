import requests

def update_salesforce_record(instance_url: str, access_token: str, object_api_name: str, record_id: str, update_data: dict) -> dict:
    url = f"{instance_url}/services/data/v59.0/sobjects/{object_api_name}/{record_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, headers=headers, json=update_data)
        if response.status_code == 204:
            return {
                "success": True,
                "message": f"Record {record_id} updated successfully.",
                "object": object_api_name
            }
        else:
            return {
                "success": False,
                "message": "Failed to update record.",
                "status_code": response.status_code,
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Request exception occurred.",
            "error": str(e)
        }