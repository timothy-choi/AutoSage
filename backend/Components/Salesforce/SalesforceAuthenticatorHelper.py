import requests
from typing import Optional

def authenticate_with_username_password(client_id: str, client_secret: str, username: str, password: str, security_token: str) -> dict:
    url = "https://login.salesforce.com/services/oauth2/token"
    payload = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password + security_token,
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return {
            "success": True,
            "auth_data": response.json()
        }
    else:
        return {
            "success": False,
            "error": response.json()
        }

def authenticate_with_refresh_token(client_id: str, client_secret: str, refresh_token: str) -> dict:
    url = "https://login.salesforce.com/services/oauth2/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return {
            "success": True,
            "auth_data": response.json()
        }
    else:
        return {
            "success": False,
            "error": response.json()
        }