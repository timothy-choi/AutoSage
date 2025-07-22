import requests
from collections import defaultdict

FIGMA_API_BASE = "https://api.figma.com/v1"

def fetch_figma_file(figma_token, file_key):
    headers = {"X-Figma-Token": figma_token}
    url = f"{FIGMA_API_BASE}/files/{file_key}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def extract_component_usage(document, path=""):
    usage = defaultdict(list)

    def traverse(node, current_path):
        if 'type' in node and node['type'] == 'INSTANCE' and 'componentId' in node:
            comp_id = node['componentId']
            usage[comp_id].append(current_path + "/" + node.get("name", "Unnamed"))

        for child in node.get("children", []):
            traverse(child, current_path + "/" + node.get("name", "Unnamed"))

    traverse(document, path)
    return usage

def fetch_component_metadata(figma_token, file_key, component_ids):
    headers = {"X-Figma-Token": figma_token}
    ids_str = ",".join(component_ids)
    url = f"{FIGMA_API_BASE}/files/{file_key}/components"
    params = {"ids": ids_str}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json().get("meta", {}).get("components", [])

def analyze_component_usage(figma_token, file_key):
    file_data = fetch_figma_file(figma_token, file_key)
    document = file_data["document"]

    usage_map = extract_component_usage(document)
    component_ids = list(usage_map.keys())
    metadata = fetch_component_metadata(figma_token, file_key, component_ids)

    result = []
    meta_dict = {comp["node_id"]: comp for comp in metadata}

    for comp_id, usage_locations in usage_map.items():
        meta = meta_dict.get(comp_id, {})
        result.append({
            "component_id": comp_id,
            "name": meta.get("name", "Unknown"),
            "description": meta.get("description", ""),
            "usage_count": len(usage_locations),
            "used_in": usage_locations
        })

    return result