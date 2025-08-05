import requests

def run_soql_query(instance_url: str, access_token: str, query: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/query"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "q": query
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "records": data.get("records", []),
            "done": data.get("done", False),
            "nextRecordsUrl": data.get("nextRecordsUrl", None)
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "SOQL query failed"
        }