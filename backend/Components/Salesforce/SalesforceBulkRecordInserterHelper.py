import requests

def bulk_insert_salesforce_records(instance_url: str, access_token: str, object_api_name: str, records: list) -> dict:
    url = f"{instance_url}/services/data/v59.0/composite/sobjects"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "allOrNone": False,
        "records": [
            {
                "attributes": {"type": object_api_name},
                **record
            } for record in records
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return {
                "success": True,
                "inserted_count": sum(1 for r in response.json() if r.get("success")),
                "results": response.json()
            }
        else:
            return {
                "success": False,
                "message": "Failed to insert records.",
                "status_code": response.status_code,
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Request exception occurred.",
            "error": str(e)
        }