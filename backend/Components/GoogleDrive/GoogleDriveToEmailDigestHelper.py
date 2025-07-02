import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_drive_digest_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    to_email: str,
    from_email: str,
    subject: str,
    files: list
) -> dict:
    if not files:
        return {"status": "skipped", "message": "No files to include"}

    html = "<h2>📁 Google Drive Digest</h2><ul>"
    for f in files:
        name = f.get("name", "Unnamed file")
        link = f.get("webViewLink", "#")
        mime = f.get("mimeType", "Unknown type")
        size = int(f.get("size", 0)) / (1024 * 1024)
        size_str = f"{size:.2f} MB" if size else "Unknown size"
        html += f"<li><b>{name}</b> ({mime}, {size_str})<br><a href='{link}'>Open</a></li><br>"
    html += "</ul>"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email
    message.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, message.as_string())
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

    return {"status": "success", "message": f"{len(files)} file(s) included in email"}