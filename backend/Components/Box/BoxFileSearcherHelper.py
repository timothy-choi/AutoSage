from boxsdk import Client
from typing import List, Dict, Optional

def search_files(
    client: Client,
    query: str,
    ancestor_folder_id: Optional[str] = None,
    file_extensions: Optional[List[str]] = None,
    limit: int = 100
) -> List[Dict]:
    search_params = {
        "query": query,
        "limit": limit,
        "type": "file"
    }
    if ancestor_folder_id:
        search_params["ancestor_folder_ids"] = [ancestor_folder_id]
    if file_extensions:
        search_params["content_types"] = ["name"]
        search_params["file_extensions"] = file_extensions

    results = client.search().query(**search_params)
    files = []
    for f in results:
        files.append({
            "id": f.id,
            "name": f.name,
            "type": f.type,
            "path_collection": [{"id": p.id, "name": p.name} for p in f.path_collection["entries"]] if f.path_collection else []
        })
    return files