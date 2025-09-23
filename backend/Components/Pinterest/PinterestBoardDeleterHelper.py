import requests

BASE_URL = "https://api.pinterest.com/v5/boards"

def delete_board(access_token: str, board_id: str):
    url = f"{BASE_URL}/{board_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code != 204:
        raise Exception(f"Failed to delete board: {response.text}")
    
    return {"message": "Board deleted successfully"}