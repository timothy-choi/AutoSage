import requests

def execute_apex_anonymous(instance_url: str, access_token: str, apex_code: str) -> dict:
    url = f"{instance_url}/services/data/v58.0/tooling/executeAnonymous"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "anonymousBody": apex_code
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to execute Apex code"
        }