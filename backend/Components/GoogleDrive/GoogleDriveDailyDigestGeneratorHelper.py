import requests
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def fetch_recent_files(access_token: str, since_iso: str) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}
    query = f"modifiedTime >= '{since_iso}' and trashed = false"
    params = {
        "q": query,
        "fields": "files(id,name,mimeType,size,modifiedTime,webViewLink)",
        "pageSize": 100
    }

    r = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(f"Failed to fetch recent files: {r.text}")
    return r.json().get("files", [])

def generate_digest_html(files: list) -> str:
    html = "<h2>📁 Google Drive Daily Digest</h2><ul>"
    for f in files:
        html += (
            f"<li><b>{f.get('name')}</b> "
            f"({f.get('mimeType')}, {int(f.get('size', 0)) / (1024*1024):.2f} MB) "
            f"- Modified: {f.get('modifiedTime')} "
            f"- <a href='{f.get('webViewLink')}'>View</a></li><br>"
        )
    html += "</ul>"
    return html

def send_email_digest(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    from_email: str,
    to_email: str,
    subject: str,
    html_content: str
) -> dict:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())

    return {"status": "success", "sent_to": to_email}

def send_slack_digest(slack_webhook_url: str, html_digest: str) -> dict:
    text = f"📁 *Google Drive Daily Digest*\n\n{html_digest}"
    response = requests.post(slack_webhook_url, json={"text": text})
    if response.status_code != 200:
        raise Exception(f"Failed to send Slack digest: {response.text}")
    return {"status": "success", "channel": "slack"}