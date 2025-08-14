import requests

def delete_trello_board(api_key, token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/closed"

    params = {
        "key": api_key,
        "token": token,
        "value": "true"
    }

    response = requests.put(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to close Trello board: {response.text}")

    return response.json()