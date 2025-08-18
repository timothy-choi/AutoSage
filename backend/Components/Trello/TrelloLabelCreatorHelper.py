import requests

def create_label(api_key, token, board_id, label_name, label_color):
    url = "https://api.trello.com/1/labels"
    params = {
        "key": api_key,
        "token": token,
        "idBoard": board_id,
        "name": label_name,
        "color": label_color
    }

    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to create label: {response.text}")

    return response.json()