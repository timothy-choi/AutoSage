import requests

def assign_permission_set(instance_url: str, access_token: str, user_id: str, permission_set_id: str) -> dict:
    url = f"{instance_url}/services/data/v58.0/sobjects/PermissionSetAssignment"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "AssigneeId": user_id,
        "PermissionSetId": permission_set_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            return {"success": True, "assignment_id": response.json().get("id")}
        else:
            return {"success": False, "error": response.text}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}