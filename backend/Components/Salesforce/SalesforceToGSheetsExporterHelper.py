import requests
import google.auth
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def fetch_salesforce_records(instance_url, access_token, object_type, fields, limit=100):
    query = f"SELECT {', '.join(fields)} FROM {object_type} LIMIT {limit}"
    url = f"{instance_url}/services/data/v60.0/query/?q={query}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Salesforce query failed: {response.text}")

    return response.json().get("records", [])

def get_sheets_service(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets"]):
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    service = build('sheets', 'v4', credentials=credentials)
    return service

def export_to_gsheet(service, spreadsheet_id, sheet_name, records, fields):
    values = [fields]  
    for record in records:
        row = [record.get(f, "") for f in fields]
        values.append(row)

    body = {
        "values": values
    }

    range_ = f"{sheet_name}!A1"
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption="RAW",
        body=body
    ).execute()