import requests

def delete_label(label_id: str, api_key: str, token: str):
    url = f"https://api.trello.com/1/labels/{label_id}"
    params = {
        "key": api_key,
        "token": token
    }

    response = requests.delete(url, params=params)
    response.raise_for_status()
    return {"message": "Label deleted successfully."}