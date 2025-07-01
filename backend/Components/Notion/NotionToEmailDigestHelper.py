import requests
import smtplib
from typing import List, Dict
from email.mime.text import MIMEText
from datetime import datetime

NOTION_API = "https://api.notion.com/v1/databases"
NOTION_QUERY = "https://api.notion.com/v1/databases/{}/query"
NOTION_VERSION = "2022-06-28"

def fetch_recent_notion_entries(notion_token: str, database_id: str, max_entries: int = 10) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    response = requests.post(NOTION_QUERY.format(database_id), headers=headers, json={"page_size": max_entries})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Notion entries: {response.text}")
    
    return response.json().get("results", [])

def format_digest(entries: List[Dict]) -> str:
    if not entries:
        return "No recent updates from Notion."

    lines = ["📝 Notion Digest\n", f"Generated: {datetime.utcnow().isoformat()} UTC\n\n"]
    for entry in entries:
        props = entry.get("properties", {})
        title_prop = props.get("Name") or props.get("Title")
        title = title_prop.get("title", [{}])[0].get("plain_text", "Untitled") if title_prop else "Untitled"
        last_edited = entry.get("last_edited_time", "Unknown")
        url = entry.get("url", "#")
        lines.append(f"• *{title}*\n  Last edited: {last_edited}\n  Link: {url}\n")

    return "\n".join(lines)

def send_email_digest(smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str,
                      sender_email: str, recipient_email: str, subject: str, body: str) -> dict:
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return {"status": 200, "message": "Digest sent successfully"}
    except Exception as e:
        return {"status": 500, "error": str(e)}

def run_notion_to_email_digest(notion_token: str, database_id: str, smtp_info: Dict, email_info: Dict) -> dict:
    entries = fetch_recent_notion_entries(notion_token, database_id)
    digest = format_digest(entries)
    return send_email_digest(
        smtp_host=smtp_info["host"],
        smtp_port=smtp_info["port"],
        smtp_user=smtp_info["username"],
        smtp_password=smtp_info["password"],
        sender_email=email_info["from"],
        recipient_email=email_info["to"],
        subject=email_info.get("subject", "Your Notion Digest"),
        body=digest
    )