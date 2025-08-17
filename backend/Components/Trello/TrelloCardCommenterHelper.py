import requests

def comment_on_trello_card(api_key, token, card_id, comment_text):
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    params = {
        "key": api_key,
        "token": token,
        "text": comment_text
    }

    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to comment on card: {response.text}")

    return response.json()