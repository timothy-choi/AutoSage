import requests

def create_notion_page(notion_token: str, database_id: str, title: str, content: str, figma_url: str) -> dict:
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    data = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }]
                }
            },
            {
                "object": "block",
                "type": "bookmark",
                "bookmark": {
                    "url": figma_url
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        return {"status": "success", "page_id": response.json().get("id")}
    else:
        return {
            "status": "error",
            "message": f"Failed to create Notion page: {response.status_code}",
            "details": response.text
        }

def format_figma_comment_entry(commenter: str, file_name: str, comment_text: str) -> str:
    return f"{commenter} left a comment on *{file_name}*:\n\n{comment_text}"

def format_figma_update_entry(file_name: str, last_modified: str) -> str:
    return f"File *{file_name}* was updated.\nLast modified: {last_modified}"