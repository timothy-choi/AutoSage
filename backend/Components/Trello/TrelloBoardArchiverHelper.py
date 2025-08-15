import requests

def archive_trello_board(api_key, token, board_id, archive_lists=False):
    lists_url = f"https://api.trello.com/1/boards/{board_id}/lists"
    lists_params = {"key": api_key, "token": token}
    lists_resp = requests.get(lists_url, params=lists_params)
    
    if lists_resp.status_code != 200:
        raise Exception(f"Failed to get lists: {lists_resp.text}")
    
    lists = lists_resp.json()

    results = []

    for lst in lists:
        list_id = lst["id"]

        cards_url = f"https://api.trello.com/1/lists/{list_id}/archiveAllCards"
        cards_resp = requests.post(cards_url, params={"key": api_key, "token": token})
        
        if cards_resp.status_code != 200:
            raise Exception(f"Failed to archive cards in list {list_id}: {cards_resp.text}")
        
        results.append({"list_id": list_id, "cards_archived": True})

        if archive_lists:
            list_archive_url = f"https://api.trello.com/1/lists/{list_id}/closed"
            archive_resp = requests.put(list_archive_url, params={
                "key": api_key,
                "token": token,
                "value": "true"
            })

            if archive_resp.status_code != 200:
                raise Exception(f"Failed to archive list {list_id}: {archive_resp.text}")

            results[-1]["list_archived"] = True

    return results