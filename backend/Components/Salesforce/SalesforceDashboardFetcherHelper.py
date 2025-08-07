import requests

def fetch_salesforce_dashboard(instance_url: str, access_token: str, dashboard_id: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/analytics/dashboards/{dashboard_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "success": True,
            "dashboard_data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to fetch dashboard data from Salesforce"
        }