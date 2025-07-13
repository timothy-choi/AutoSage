import requests
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

DROPBOX_LIST_FOLDER_URL = "https://api.dropboxapi.com/2/files/list_folder"

def fetch_recent_files(access_token: str, folder_path: str = "", hours: int = 24) -> list:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "path": folder_path,
        "recursive": True,
        "include_deleted": False
    }

    res = requests.post(DROPBOX_LIST_FOLDER_URL, headers=headers, json=payload)
    if res.status_code != 200:
        raise Exception(f"Dropbox API error: {res.text}")

    entries = res.json().get("entries", [])
    cutoff = datetime.utcnow() - timedelta(hours=hours)

    return [
        {
            "name": f["name"],
            "path": f["path_display"],
            "size": f["size"],
            "client_modified": f["client_modified"]
        }
        for f in entries if f[".tag"] == "file" and datetime.fromisoformat(f["client_modified"].replace("Z", "+00:00")) >= cutoff
    ]


def format_digest_html(files: list) -> str:
    if not files:
        return "<p>No new files found.</p>"

    html = "<h2>📬 Dropbox Upload Digest</h2><ul>"
    for f in files:
        html += f"<li><b>{f['name']}</b> — {f['size']:,} bytes<br><i>{f['path']}</i><br>{f['client_modified']}</li>"
    html += "</ul>"
    return html


def send_email_digest(smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str,
                      sender: str, recipient: str, subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())


def generate_and_send_dropbox_digest(
    access_token: str,
    folder_path: str,
    hours: int,
    send_email: bool,
    smtp_config: dict = None
) -> dict:
    files = fetch_recent_files(access_token, folder_path, hours)
    html = format_digest_html(files)

    if send_email and smtp_config:
        send_email_digest(
            smtp_host=smtp_config["smtp_host"],
            smtp_port=smtp_config["smtp_port"],
            smtp_user=smtp_config["smtp_user"],
            smtp_password=smtp_config["smtp_password"],
            sender=smtp_config["sender"],
            recipient=smtp_config["recipient"],
            subject="📬 Dropbox Upload Digest",
            html_body=html
        )

    return {
        "files_found": len(files),
        "email_sent": send_email,
        "digest_html": html
    }