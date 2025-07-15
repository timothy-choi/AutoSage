import requests

DROPBOX_QUOTA_URL = "https://api.dropboxapi.com/2/users/get_space_usage"

def format_bytes(size: int) -> str:
    """Convert bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def fetch_dropbox_quota(access_token: str, human_readable: bool = False) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    res = requests.post(DROPBOX_QUOTA_URL, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Dropbox API error: {res.text}")

    data = res.json()
    used = data["used"]
    allocated = data["allocation"]["allocated"]

    available = allocated - used
    usage_percent = (used / allocated) * 100

    if human_readable:
        return {
            "used": format_bytes(used),
            "available": format_bytes(available),
            "allocated": format_bytes(allocated),
            "usage_percent": f"{usage_percent:.2f}%"
        }
    else:
        return {
            "used_bytes": used,
            "available_bytes": available,
            "allocated_bytes": allocated,
            "usage_percent": usage_percent
        }