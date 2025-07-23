import requests

def delete_confluence_page(base_url: str, username: str, api_token: str, page_id: str) -> bool:
    url = f"{base_url}/rest/api/content/{page_id}"
    auth = (username, api_token)
    headers = {"Content-Type": "application/json"}

    response = requests.delete(url, auth=auth, headers=headers)
    return response.status_code == 204


def delete_multiple_confluence_pages(base_url: str, username: str, api_token: str, page_ids: list) -> list:
    results = []
    for page_id in page_ids:
        try:
            success = delete_confluence_page(base_url, username, api_token, page_id)
            results.append({
                "page_id": page_id,
                "status": "deleted" if success else "failed"
            })
        except Exception as e:
            results.append({
                "page_id": page_id,
                "status": "error",
                "message": str(e)
            })
    return results