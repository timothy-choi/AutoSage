import requests

def run_sosl_query(instance_url: str, access_token: str, sosl: str) -> dict:
    url = f"{instance_url}/services/data/v59.0/search"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "q": sosl
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return {
            "success": True,
            "results": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "SOSL query failed"
        }