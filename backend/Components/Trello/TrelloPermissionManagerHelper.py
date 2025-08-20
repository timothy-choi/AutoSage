import requests

def update_member_permission(board_id: str, member_id: str, permission_level: str, api_key: str, token: str):
    if permission_level not in {"normal", "admin", "observer"}:
        raise ValueError("Invalid permission level. Must be 'normal', 'admin', or 'observer'.")

    url = f"https://api.trello.com/1/boards/{board_id}/members/{member_id}"
    params = {
        "key": api_key,
        "token": token,
        "type": permission_level
    }

    response = requests.put(url, params=params)
    response.raise_for_status()
    return {"message": f"Member {member_id} updated to '{permission_level}' on board {board_id}."}