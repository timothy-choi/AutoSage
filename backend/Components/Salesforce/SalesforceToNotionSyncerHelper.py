import requests

def fetch_salesforce_records(instance_url, access_token, object_type, fields, limit=10):
    query = f"SELECT {', '.join(fields)} FROM {object_type} LIMIT {limit}"
    url = f"{instance_url}/services/data/v60.0/query/?q={query}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Salesforce query failed: {response.text}")
    
    return response.json().get("records", [])


def create_notion_page(notion_token, database_id, record, field_mapping):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    properties = {}
    for notion_key, salesforce_field in field_mapping.items():
        properties[notion_key] = {
            "title": [{"text": {"content": str(record.get(salesforce_field, ''))}}]
        }

    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Notion page creation failed: {response.text}")

    return response.json()