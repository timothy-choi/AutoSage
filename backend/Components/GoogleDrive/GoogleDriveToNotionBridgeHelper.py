import requests

def send_drive_files_to_notion(
    files: list,
    notion_token: str,
    database_id: str
) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    success_count = 0
    for file in files:
        name = file.get("name", "Untitled")
        mime = file.get("mimeType", "Unknown")
        link = file.get("webViewLink", "")
        size_mb = f"{int(file.get('size', 0)) / (1024 * 1024):.2f} MB" if file.get("size") else "Unknown"

        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": name}}]
                },
                "Type": {
                    "rich_text": [{"text": {"content": mime}}]
                },
                "Size": {
                    "rich_text": [{"text": {"content": size_mb}}]
                },
                "Link": {
                    "url": link
                }
            }
        }

        res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
        if res.status_code not in (200, 201):
            raise Exception(f"Notion error: {res.text}")
        success_count += 1

    return {
        "status": "success",
        "message": f"{success_count} file(s) added to Notion"
    }