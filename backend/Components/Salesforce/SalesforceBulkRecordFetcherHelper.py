import requests

def fetch_salesforce_bulk_records(instance_url: str, access_token: str, object_api_name: str, fields: list, where_clause: str = "", limit: int = 2000) -> dict:
    base_url = f"{instance_url}/services/data/v59.0/query"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    field_str = ', '.join(fields)
    query = f"SELECT {field_str} FROM {object_api_name}"
    if where_clause:
        query += f" WHERE {where_clause}"
    query += f" LIMIT {limit}"

    params = {"q": query}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "records": data.get("records", []),
            "done": data.get("done", False),
            "next_url": data.get("nextRecordsUrl")
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Failed to fetch records.",
            "error": str(e)
        }


def fetch_salesforce_next_records(instance_url: str, access_token: str, next_url: str) -> dict:
    url = f"{instance_url}{next_url}"
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
            "records": data.get("records", []),
            "done": data.get("done", False),
            "next_url": data.get("nextRecordsUrl")
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": "Failed to fetch next page.",
            "error": str(e)
        }