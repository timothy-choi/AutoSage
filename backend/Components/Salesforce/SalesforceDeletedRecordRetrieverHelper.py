import requests
from datetime import datetime

def retrieve_deleted_salesforce_records(instance_url: str, access_token: str, object_api_name: str, start_time: str, end_time: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/sobjects/{object_api_name}/deleted/?start={start_time}&end={end_time}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "deletedRecords": data.get("deletedRecords", []),
            "earliestDateAvailable": data.get("earliestDateAvailable"),
            "latestDateCovered": data.get("latestDateCovered")
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve deleted records from Salesforce."
        }