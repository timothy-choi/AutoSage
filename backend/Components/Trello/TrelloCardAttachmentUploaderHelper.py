import requests

def upload_file_attachment(api_key, token, card_id, file_path):
    url = f"https://api.trello.com/1/cards/{card_id}/attachments"
    params = {
        "key": api_key,
        "token": token
    }

    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, params=params, files=files)

    if response.status_code != 200:
        raise Exception(f"Failed to upload file: {response.text}")

    return response.json()


def attach_url(api_key, token, card_id, url_to_attach, name=None):
    url = f"https://api.trello.com/1/cards/{card_id}/attachments"
    params = {
        "key": api_key,
        "token": token,
        "url": url_to_attach
    }
    if name:
        params["name"] = name

    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to attach URL: {response.text}")

    return response.json()