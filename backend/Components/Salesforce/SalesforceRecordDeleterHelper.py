import requests

def delete_salesforce_record(instance_url: str, access_token: str, object_api_name: str, record_id: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/sobjects/{object_api_name}/{record_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return {
                "success": True,
                "message": f"Record {record_id} deleted successfully.",
                "object": object_api_name
            }
        else:
            return {
                "success": False,
                "message": f"Failed to delete record {record_id}.",
                "status_code": response.status_code,
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Request exception occurred.",
            "error": str(e)
        }