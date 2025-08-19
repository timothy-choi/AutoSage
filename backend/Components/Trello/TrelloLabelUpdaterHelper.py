import requests

def update_label(label_id, name=None, color=None, api_key=None, token=None):
    url = f"https://api.trello.com/1/labels/{label_id}"
    params = {
        "key": api_key,
        "token": token,
    }

    if name is not None:
        params["name"] = name
    if color is not None:
        params["color"] = color

    response = requests.put(url, params=params)
    return response.json()