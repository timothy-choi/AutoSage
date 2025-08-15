import requests

def create_trello_list(api_key, token, board_id, name, pos="bottom"):
    url = "https://api.trello.com/1/lists"
    params = {
        "key": api_key,
        "token": token,
        "idBoard": board_id,
        "name": name,
        "pos": pos
    }

    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to create list: {response.text}")

    return response.json()