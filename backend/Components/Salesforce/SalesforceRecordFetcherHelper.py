import requests

def fetch_salesforce_records(instance_url: str, access_token: str, soql_query: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/query"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "q": soql_query
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return {
                "success": True,
                "records": response.json().get("records", []),
                "totalSize": response.json().get("totalSize", 0),
                "done": response.json().get("done", False),
                "nextRecordsUrl": response.json().get("nextRecordsUrl")
            }
        elif response.status_code == 400:
            return {
                "success": False,
                "message": "Invalid SOQL query.",
                "status_code": 400,
                "details": response.text
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "message": "Unauthorized. Check access token.",
                "status_code": 401
            }
        else:
            return {
                "success": False,
                "message": "Failed to fetch records.",
                "status_code": response.status_code,
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Request failed.",
            "error": str(e)
        }