import requests
from config import (
    CONFLUENCE_API_BASE,
    CONFLUENCE_API_HEADERS,
    JIRA_API_BASE,
    JIRA_API_HEADERS
)

def add_jira_link_to_confluence_page(page_id: str, jira_issue_key: str) -> dict:
    try:
        jira_link_markup = f'<ac:structured-macro ac:name="jira"><ac:parameter ac:name="key">{jira_issue_key}</ac:parameter></ac:structured-macro>'
        
        page_url = f"{CONFLUENCE_API_BASE}/content/{page_id}?expand=body.storage,version"
        page_response = requests.get(page_url, headers=CONFLUENCE_API_HEADERS)
        page_response.raise_for_status()
        page_data = page_response.json()

        current_content = page_data["body"]["storage"]["value"]
        new_content = current_content + "<p>Linked Jira issue:</p>" + jira_link_markup

        update_payload = {
            "id": page_id,
            "type": "page",
            "title": page_data["title"],
            "version": {
                "number": page_data["version"]["number"] + 1
            },
            "body": {
                "storage": {
                    "value": new_content,
                    "representation": "storage"
                }
            }
        }

        update_url = f"{CONFLUENCE_API_BASE}/content/{page_id}"
        update_response = requests.put(update_url, headers=CONFLUENCE_API_HEADERS, json=update_payload)
        update_response.raise_for_status()

        return {"success": True, "message": f"Linked Jira issue {jira_issue_key} to Confluence page {page_id}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def comment_on_jira_issue(jira_issue_key: str, confluence_page_url: str) -> dict:
    try:
        url = f"{JIRA_API_BASE}/issue/{jira_issue_key}/comment"
        payload = {
            "body": f"This issue is referenced in the following Confluence page: {confluence_page_url}"
        }
        response = requests.post(url, headers=JIRA_API_HEADERS, json=payload)
        response.raise_for_status()
        return {"success": True, "message": f"Comment added to Jira issue {jira_issue_key}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def link_confluence_to_jira(page_id: str, jira_issue_key: str, confluence_base_url: str) -> dict:
    confluence_link_result = add_jira_link_to_confluence_page(page_id, jira_issue_key)
    if not confluence_link_result["success"]:
        return confluence_link_result

    page_url = f"{confluence_base_url}/pages/viewpage.action?pageId={page_id}"
    jira_comment_result = comment_on_jira_issue(jira_issue_key, page_url)

    return {
        "success": True,
        "confluence_result": confluence_link_result,
        "jira_result": jira_comment_result
    }