import csv
import json
from typing import List
from fastapi import UploadFile

def track_linkedin_follower_changes(old_followers: List[str], new_followers: List[str]) -> dict:
    old_set = set(old_followers)
    new_set = set(new_followers)

    gained = sorted(new_set - old_set)
    lost = sorted(old_set - new_set)
    unchanged = sorted(new_set & old_set)

    return {
        "gained_followers": gained,
        "lost_followers": lost,
        "unchanged_followers": unchanged,
        "total_now": len(new_followers),
        "total_before": len(old_followers)
    }


async def parse_follower_file(file: UploadFile) -> List[str]:
    contents = await file.read()

    if file.filename.endswith(".csv"):
        decoded = contents.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded)
        keys = reader.fieldnames or []
        key = "Full Name" if "Full Name" in keys else "Name" if "Name" in keys else keys[0]
        return [row.get(key, "").strip() for row in reader if row.get(key)]

    elif file.filename.endswith(".json"):
        data = json.loads(contents)
        if isinstance(data, list):
            if isinstance(data[0], str):
                return data
            elif isinstance(data[0], dict):
                key = "name" if "name" in data[0] else "urn" if "urn" in data[0] else list(data[0].keys())[0]
                return [entry.get(key, "").strip() for entry in data if key in entry]
    return []