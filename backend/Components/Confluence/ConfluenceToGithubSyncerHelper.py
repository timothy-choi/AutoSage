import requests
import base64
from config import CONFLUENCE_API_BASE, CONFLUENCE_API_HEADERS, GITHUB_API_BASE, GITHUB_API_HEADERS

def fetch_confluence_page(page_id: str) -> dict:
    url = f"{CONFLUENCE_API_BASE}/content/{page_id}?expand=body.storage,title"
    response = requests.get(url, headers=CONFLUENCE_API_HEADERS)
    response.raise_for_status()
    data = response.json()
    return {
        "title": data["title"],
        "content": data["body"]["storage"]["value"]
    }

def get_github_file_sha(owner: str, repo: str, path: str) -> str:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=GITHUB_API_HEADERS)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def push_to_github(owner: str, repo: str, path: str, content: str, commit_message: str, branch: str = "main") -> dict:
    sha = get_github_file_sha(owner, repo, path)
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch
    }
    if sha:
        payload["sha"] = sha

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    response = requests.put(url, headers=GITHUB_API_HEADERS, json=payload)
    if response.status_code in [200, 201]:
        return {"success": True, "data": response.json()}
    return {"success": False, "error": response.text}

def sync_confluence_to_github(page_id: str, owner: str, repo: str, filepath: str, branch: str = "main") -> dict:
    try:
        confluence_data = fetch_confluence_page(page_id)
        commit_msg = f"Sync Confluence page '{confluence_data['title']}'"
        return push_to_github(owner, repo, filepath, confluence_data["content"], commit_msg, branch)
    except Exception as e:
        return {"success": False, "error": str(e)}