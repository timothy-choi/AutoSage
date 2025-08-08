import requests

def invoke_apex_rest(
    instance_url: str,
    access_token: str,
    endpoint_path: str,
    method: str = "GET",
    payload: dict = None,
    params: dict = None
) -> dict:
    url = f"{instance_url}{endpoint_path}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=payload,
            params=params
        )
        response.raise_for_status()
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.content else {}
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to invoke Apex REST endpoint: {endpoint_path}"
        }