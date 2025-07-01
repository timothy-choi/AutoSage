import requests

def search_jira_mentions(jira_domain, jira_email, jira_token, username_or_account_id, max_results=10):
    headers = {
        "Authorization": f"Basic {requests.auth._basic_auth_str(jira_email, jira_token)}",
        "Accept": "application/json"
    }

    mentions = []

    jql = f'text ~ "@{username_or_account_id}"'
    search_url = f"https://{jira_domain}/rest/api/3/search"
    params = {
        "jql": jql,
        "maxResults": max_results,
        "fields": "summary,description"
    }

    search_response = requests.get(search_url, headers=headers, params=params)
    if search_response.status_code != 200:
        raise Exception(f"Jira search error: {search_response.text}")

    issues = search_response.json().get("issues", [])
    for issue in issues:
        mentions.append({
            "issue_key": issue["key"],
            "location": "issue",
            "summary": issue["fields"]["summary"],
            "url": f"https://{jira_domain}/browse/{issue['key']}"
        })

    for issue in issues:
        issue_key = issue["key"]
        comment_url = f"https://{jira_domain}/rest/api/3/issue/{issue_key}/comment"
        comment_response = requests.get(comment_url, headers=headers)

        if comment_response.status_code != 200:
            continue

        comments = comment_response.json().get("comments", [])
        for comment in comments:
            body = comment.get("body", "")
            if f"@{username_or_account_id}" in body:
                mentions.append({
                    "issue_key": issue_key,
                    "location": "comment",
                    "comment_id": comment.get("id"),
                    "text": body,
                    "author": comment.get("author", {}).get("displayName"),
                    "url": f"https://{jira_domain}/browse/{issue_key}?focusedCommentId={comment['id']}"
                })

    return mentions