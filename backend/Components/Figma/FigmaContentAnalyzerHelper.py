import requests

def analyze_figma_content(file_key: str, access_token: str) -> dict:
    headers = {
        "X-Figma-Token": access_token
    }

    file_url = f"https://api.figma.com/v1/files/{file_key}"
    response = requests.get(file_url, headers=headers)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch file data",
            "details": response.json()
        }

    file_data = response.json()
    document = file_data.get("document", {})
    stats = {
        "frames": 0,
        "components": 0,
        "text_nodes": 0,
        "images": 0,
        "total_nodes": 0
    }

    def traverse(node):
        stats["total_nodes"] += 1
        node_type = node.get("type")
        if node_type == "FRAME":
            stats["frames"] += 1
        elif node_type == "COMPONENT":
            stats["components"] += 1
        elif node_type == "TEXT":
            stats["text_nodes"] += 1
        elif node_type == "IMAGE":
            stats["images"] += 1

        for child in node.get("children", []):
            traverse(child)

    traverse(document)

    return {
        "status": "success",
        "file_name": file_data.get("name", "unknown"),
        "stats": stats
    }