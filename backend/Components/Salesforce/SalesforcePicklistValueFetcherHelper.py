import requests

def fetch_picklist_values(instance_url: str, access_token: str, object_api_name: str, field_api_name: str) -> dict:
    url = (
        f"{instance_url}/services/data/v59.0/ui-api/object-info/{object_api_name}/picklist-values/012000000000000AAA/{field_api_name}"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            values = data.get("values", [])
            return {
                "success": True,
                "field": field_api_name,
                "object": object_api_name,
                "picklist_values": [val.get("label") for val in values]
            }
        elif response.status_code == 403:
            return {
                "success": False,
                "message": "Permission denied or UI API access not enabled.",
                "status_code": 403
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "message": "Field or object not found.",
                "status_code": 404
            }
        else:
            return {
                "success": False,
                "message": "Failed to fetch picklist values.",
                "status_code": response.status_code,
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Request failed.",
            "error": str(e)
        }