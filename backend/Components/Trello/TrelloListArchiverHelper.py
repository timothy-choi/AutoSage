import requests

def archive_trello_list(api_key, token, list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/closed"
    params = {
        "key": api_key,
        "token": token,
        "value": "true"
    }

    response = requests.put(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to archive list: {response.text}")

    return response.json()