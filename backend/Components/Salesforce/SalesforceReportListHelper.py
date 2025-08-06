import requests

def list_salesforce_reports(instance_url: str, access_token: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/analytics/reports"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "success": True,
            "reports": response.json().get("reports", [])
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to fetch reports from Salesforce"
        }