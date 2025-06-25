import requests
from requests.auth import HTTPBasicAuth
import openai 

def generate_smart_jira_reply(
    issue_summary: str,
    issue_description: str,
    comment_text: str,
    openai_api_key: str,
    model: str = "gpt-4"
) -> str:
    openai.api_key = openai_api_key

    prompt = f"""
You are a helpful assistant for a Jira issue tracker.
Given the issue summary, description, and a user's comment, generate a concise and helpful reply.

Issue Summary: {issue_summary}
Issue Description: {issue_description}
User Comment: {comment_text}

Your Response:
    """.strip()

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()


def post_comment_to_jira(
    jira_base_url: str,
    email: str,
    api_token: str,
    issue_key: str,
    comment: str
) -> dict:
    url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/comment"
    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "body": comment
    }

    response = requests.post(url, headers=headers, json=payload, auth=auth)

    if response.status_code == 201:
        return {
            "status": "posted",
            "comment_id": response.json()["id"],
            "comment": comment
        }

    return {
        "status": "error",
        "code": response.status_code,
        "message": response.text
    }