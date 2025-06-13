import aiohttp

async def create_jira_ticket(jira_url: str, auth_token: str, project_key: str, summary: str, description: str, issue_type: str = "Task") -> dict:
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{jira_url}/rest/api/2/issue", json=payload, headers=headers) as resp:
            if resp.status == 201:
                return await resp.json()
            return {"error": f"Failed to create ticket: HTTP {resp.status}"}

async def add_comment_to_ticket(jira_url: str, auth_token: str, issue_key: str, comment: str) -> dict:
    payload = {"body": comment}
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{jira_url}/rest/api/2/issue/{issue_key}/comment", json=payload, headers=headers) as resp:
            if resp.status == 201:
                return await resp.json()
            return {"error": f"Failed to add comment: HTTP {resp.status}"}

async def update_ticket_status(jira_url: str, auth_token: str, issue_key: str, transition_id: str) -> dict:
    payload = {"transition": {"id": transition_id}}
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{jira_url}/rest/api/2/issue/{issue_key}/transitions", json=payload, headers=headers) as resp:
            if resp.status == 204:
                return {"status": "ticket status updated"}
            return {"error": f"Failed to update status: HTTP {resp.status}"}