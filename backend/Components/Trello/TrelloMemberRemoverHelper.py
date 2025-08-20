import requests

def remove_member_from_board(board_id: str, member_id: str, api_key: str, token: str):
    url = f"https://api.trello.com/1/boards/{board_id}/members/{member_id}"
    params = {
        "key": api_key,
        "token": token
    }

    response = requests.delete(url, params=params)
    response.raise_for_status()
    return {"message": f"Member {member_id} removed from board {board_id}."}