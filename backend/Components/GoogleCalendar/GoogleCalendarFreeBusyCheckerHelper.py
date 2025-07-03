import requests
from typing import List

FREEBUSY_URL = "https://www.googleapis.com/calendar/v3/freeBusy"

def check_free_busy(
    access_token: str,
    time_min: str,
    time_max: str,
    calendar_ids: List[str]
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [{"id": cal_id} for cal_id in calendar_ids]
    }

    response = requests.post(FREEBUSY_URL, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch free/busy info: {response.text}")

    return {
        "status": "success",
        "calendars": response.json().get("calendars", {})
    }