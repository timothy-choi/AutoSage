import csv
import json
from typing import List
from fastapi import UploadFile

def track_linkedin_connection_changes(old_connections: list[str], new_connections: list[str]) -> dict:
    old_set = set(old_connections)
    new_set = set(new_connections)

    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    unchanged = sorted(new_set & old_set)

    return {
        "added_connections": added,
        "removed_connections": removed,
        "unchanged_connections": unchanged,
        "total_now": len(new_connections),
        "total_before": len(old_connections)
    }


async def parse_connection_file(file: UploadFile) -> List[str]:
    contents = await file.read()

    if file.filename.endswith(".csv"):
        decoded = contents.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded)
        keys = reader.fieldnames or []
        name_key = "Full Name" if "Full Name" in keys else "Name" if "Name" in keys else keys[0]
        return [row.get(name_key, "").strip() for row in reader if row.get(name_key)]

    elif file.filename.endswith(".json"):
        data = json.loads(contents)
        if isinstance(data, list):
            if isinstance(data[0], str):
                return data
            elif isinstance(data[0], dict):
                key = "name" if "name" in data[0] else "urn" if "urn" in data[0] else list(data[0].keys())[0]
                return [entry.get(key, "").strip() for entry in data if key in entry]
    return []