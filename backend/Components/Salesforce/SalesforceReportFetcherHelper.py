import requests

def fetch_salesforce_report(instance_url: str, access_token: str, report_id: str, include_details: bool = False) -> dict:
    detail_param = "true" if include_details else "false"
    url = f"{instance_url}/services/data/v59.0/analytics/reports/{report_id}?includeDetails={detail_param}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "success": True,
            "report_data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to fetch report data from Salesforce"
        }