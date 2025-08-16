import requests

def assign_members_to_card(api_key, token, card_id, member_ids):
    url = f"https://api.trello.com/1/cards/{card_id}/idMembers"
    params = {
        "key": api_key,
        "token": token
    }

    results = []
    for member_id in member_ids:
        member_params = {**params, "value": member_id}
        response = requests.post(url, params=member_params)
        if response.status_code != 200:
            raise Exception(f"Failed to assign member {member_id}: {response.text}")
        results.append(response.json())

    return results