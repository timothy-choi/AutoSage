import requests

def test_salesforce_connection(instance_url: str, access_token: str) -> dict:
    test_url = f"{instance_url}/services/data/v59.0/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(test_url, headers=headers)

        if response.status_code == 200:
            return {
                "success": True,
                "message": "Connection successful",
                "available_versions": response.json()
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "message": "Unauthorized — Access token may be invalid or expired",
                "status_code": 401
            }
        else:
            return {
                "success": False,
                "message": f"Unexpected response from Salesforce",
                "status_code": response.status_code,
                "details": response.text
            }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Connection failed",
            "error": str(e)
        }