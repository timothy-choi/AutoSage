import requests

def add_member_to_board(board_id: str, email: str, api_key: str, token: str, role: str = "normal"):
    url = f"https://api.trello.com/1/boards/{board_id}/members"
    params = {
        "email": email,
        "type": role,
        "key": api_key,
        "token": token
    }

    response = requests.put(url, params=params)
    response.raise_for_status()
    return {"message": "Member invited successfully to the board."}