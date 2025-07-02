import requests
from typing import Dict
from collections import Counter

NOTION_VERSION = "2022-06-28"
NOTION_QUERY_URL = "https://api.notion.com/v1/databases/{}/query"

def fetch_notion_records(notion_token: str, database_id: str, max_pages: int = 100) -> list:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    payload = {"page_size": max_pages}
    response = requests.post(NOTION_QUERY_URL.format(database_id), headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Notion data: {response.text}")
    return response.json().get("results", [])

def extract_property_values(entry: Dict, prop_name: str) -> list:
    prop = entry.get("properties", {}).get(prop_name)
    if not prop:
        return []

    if prop.get("type") == "select":
        val = prop.get("select", {}).get("name")
        return [val] if val else []

    elif prop.get("type") == "multi_select":
        return [tag.get("name") for tag in prop.get("multi_select", [])]

    elif prop.get("type") == "checkbox":
        return ["Checked" if prop.get("checkbox") else "Unchecked"]

    return []

def aggregate_property_counts(notion_token: str, database_id: str, property_name: str, max_pages: int = 100) -> Dict:
    entries = fetch_notion_records(notion_token, database_id, max_pages)
    counter = Counter()

    for entry in entries:
        values = extract_property_values(entry, property_name)
        counter.update(values)

    return {
        "property": property_name,
        "counts": dict(counter),
        "total_entries": len(entries)
    }