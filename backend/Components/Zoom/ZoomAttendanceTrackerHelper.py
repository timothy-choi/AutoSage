import requests
from datetime import datetime
from zoneinfo import ZoneInfo

def fetch_zoom_attendance(meeting_id: str, jwt_token: str) -> list:
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    params = {"page_size": 100}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch attendance: {response.text}")
    
    return response.json().get("participants", [])

def format_attendance_report(participants: list, timezone: str = "UTC") -> list:
    report = []
    for p in participants:
        join_time = p.get("join_time")
        leave_time = p.get("leave_time")
        duration = p.get("duration", 0)

        try:
            join_dt = datetime.fromisoformat(join_time.replace("Z", "+00:00")).astimezone(ZoneInfo(timezone)) if join_time else None
            leave_dt = datetime.fromisoformat(leave_time.replace("Z", "+00:00")).astimezone(ZoneInfo(timezone)) if leave_time else None
        except:
            join_dt = leave_dt = None

        report.append({
            "name": p.get("name", "Unknown"),
            "email": p.get("user_email", "N/A"),
            "join_time": join_dt.strftime("%Y-%m-%d %H:%M:%S") if join_dt else "N/A",
            "leave_time": leave_dt.strftime("%Y-%m-%d %H:%M:%S") if leave_dt else "N/A",
            "duration_minutes": duration,
            "sessions": p.get("num_sessions", 1)
        })
    return report