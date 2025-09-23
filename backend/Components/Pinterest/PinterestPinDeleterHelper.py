import requests

BASE_URL = "https://api.pinterest.com/v5"

def delete_pin(access_token: str, pin_id: str):
    url = f"{BASE_URL}/pins/{pin_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    
    if response.status_code != 204:
        raise Exception(f"Failed to delete pin: {response.text}")
    
    return {"message": "Pin deleted successfully"}