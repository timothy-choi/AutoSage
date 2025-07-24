import requests

def create_bulk_confluence_pages(
    base_url: str,
    username: str,
    api_token: str,
    space_key: str,
    pages: list
) -> dict:
    url = f"{base_url}/rest/api/content"
    auth = (username, api_token)
    headers = {
        "Content-Type": "application/json"
    }

    results = []
    for page in pages:
        title = page["title"]
        body = page["body"]
        parent_id = page.get("parent_id")

        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": body,
                    "representation": "storage"
                }
            }
        }

        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]

        response = requests.post(url, auth=auth, headers=headers, json=payload)
        result = {
            "title": title,
            "status_code": response.status_code,
            "response": response.json() if response.content else {}
        }
        results.append(result)

    return {
        "summary": {
            "total": len(pages),
            "successful": sum(1 for r in results if 200 <= r["status_code"] < 300),
            "failed": sum(1 for r in results if r["status_code"] >= 300)
        },
        "details": results
    }