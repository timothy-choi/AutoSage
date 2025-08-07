import requests

def invoke_salesforce_flow(instance_url: str, access_token: str, flow_name: str, input_variables: dict = None) -> dict:
    url = f"{instance_url}/services/data/v59.0/actions/custom/flow/{flow_name}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": [input_variables or {}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "success": True,
            "flow_result": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to invoke Salesforce Flow"
        }