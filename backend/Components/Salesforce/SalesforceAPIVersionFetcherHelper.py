import requests

def fetch_salesforce_api_versions(instance_url: str, access_token: str) -> dict:
    url = f"{instance_url}/services/data"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return {
                "success": True,
                "api_versions": response.json()
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "message": "Unauthorized. Invalid or expired access token.",
                "status_code": 401
            }
        else:
            return {
                "success": False,
                "message": "Failed to fetch API versions.",
                "status_code": response.status_code,
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Request exception occurred.",
            "error": str(e)
        }