import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_trello_board_data(api_key, token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {
        "key": api_key,
        "token": token,
        "fields": "name,desc,due,idList,url"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def export_to_google_sheets(sheet_id, worksheet_name, trello_cards, credentials_json):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    worksheet.clear()
    worksheet.append_row(["Card Name", "Description", "Due Date", "List ID", "URL"])

    for card in trello_cards:
        worksheet.append_row([
            card.get("name", ""),
            card.get("desc", ""),
            card.get("due", ""),
            card.get("idList", ""),
            card.get("url", "")
        ])