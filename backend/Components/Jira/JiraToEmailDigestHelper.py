import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def fetch_jira_issues(jira_base_url, email, api_token, jql, max_results=10):
    url = f"{jira_base_url}/rest/api/2/search"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}

    params = {
        "jql": jql,
        "maxResults": max_results,
        "fields": "summary,status,assignee"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch issues: {response.text}")

    issues = response.json()["issues"]
    return issues

def build_email_digest(issues, jira_base_url):
    rows = ""
    for issue in issues:
        key = issue["key"]
        fields = issue["fields"]
        summary = fields["summary"]
        status = fields["status"]["name"]
        assignee = fields.get("assignee", {}).get("displayName", "Unassigned")
        url = f"{jira_base_url}/browse/{key}"

        rows += f"""
        <tr>
            <td><a href="{url}">{key}</a></td>
            <td>{summary}</td>
            <td>{status}</td>
            <td>{assignee}</td>
        </tr>
        """

    return f"""
    <html>
    <body>
        <h2>Jira Issue Digest</h2>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr>
                <th>Key</th>
                <th>Summary</th>
                <th>Status</th>
                <th>Assignee</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

def send_email_smtp(sender, recipient_list, subject, html_content, smtp_server, smtp_port, smtp_username, smtp_password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipient_list)

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient_list, msg.as_string())

    return {"status": "sent", "recipients": recipient_list}