import requests
from datetime import datetime, timedelta
from typing import List

GOOGLE_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
JIRA_CREATE_ISSUE_URL = "{jira_base_url}/rest/api/3/issue"

def fetch_upcoming_events(
    access_token: str,
    calendar_id: str,
    hours_ahead: int = 24,
    max_results: int = 10
) -> List[dict]:
    now = datetime.utcnow()
    time_min = now.isoformat() + "Z"
    time_max = (now + timedelta(hours=hours_ahead)).isoformat() + "Z"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": True,
        "orderBy": "startTime",
        "maxResults": max_results
    }

    res = requests.get(
        GOOGLE_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if res.status_code != 200:
        raise Exception(f"Failed to fetch calendar events: {res.text}")

    return res.json().get("items", [])

def create_jira_issue(
    jira_base_url: str,
    jira_email: str,
    jira_api_token: str,
    project_key: str,
    event: dict
) -> dict:
    auth = (jira_email, jira_api_token)

    summary = event.get("summary", "Untitled Event")
    description = event.get("description", "No description")
    start_time = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
    location = event.get("location", "")

    full_description = f"🗓 *Start*: {start_time}\n📍 *Location*: {location}\n\n{description}"

    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": full_description,
            "issuetype": {
                "name": "Task"
            }
        }
    }

    res = requests.post(
        JIRA_CREATE_ISSUE_URL.format(jira_base_url=jira_base_url),
        auth=auth,
        json=payload
    )

    if res.status_code not in [200, 201]:
        raise Exception(f"Failed to create Jira issue: {res.text}")

    return res.json()

def push_calendar_events_to_jira(
    google_access_token: str,
    calendar_id: str,
    jira_base_url: str,
    jira_email: str,
    jira_api_token: str,
    jira_project_key: str,
    hours_ahead: int = 24,
    max_results: int = 10
) -> dict:
    events = fetch_upcoming_events(
        access_token=google_access_token,
        calendar_id=calendar_id,
        hours_ahead=hours_ahead,
        max_results=max_results
    )

    results = []

    for event in events:
        try:
            issue = create_jira_issue(
                jira_base_url=jira_base_url,
                jira_email=jira_email,
                jira_api_token=jira_api_token,
                project_key=jira_project_key,
                event=event
            )
            results.append({
                "event": event.get("summary"),
                "jira_issue_key": issue.get("key")
            })
        except Exception as e:
            results.append({
                "event": event.get("summary"),
                "error": str(e)
            })

    return {
        "status": "success",
        "synced": len(results),
        "details": results
    }