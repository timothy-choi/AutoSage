import requests

def create_trello_board(api_key, token, board_name, default_lists=True, desc=None, org_id=None, permission_level="private"):
    url = "https://api.trello.com/1/boards/"

    params = {
        "key": api_key,
        "token": token,
        "name": board_name,
        "defaultLists": str(default_lists).lower(),
        "prefs_permissionLevel": permission_level
    }

    if desc:
        params["desc"] = desc
    if org_id:
        params["idOrganization"] = org_id

    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Trello board creation failed: {response.text}")

    return response.json()