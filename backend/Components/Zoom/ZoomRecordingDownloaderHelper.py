import requests
import os

def fetch_meeting_recordings(meeting_id: str, jwt_token: str) -> list:
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"
    headers = {"Authorization": f"Bearer {jwt_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch recordings: {response.text}")

    return response.json().get("recording_files", [])

def download_recordings(recording_files: list, jwt_token: str, save_dir: str = "./zoom_recordings") -> list:
    os.makedirs(save_dir, exist_ok=True)
    results = []

    for i, file in enumerate(recording_files):
        download_url = file.get("download_url")
        if not download_url:
            continue

        file_type = file.get("file_type", "dat")
        start = file.get("recording_start", f"file_{i}")
        filename = f"{start.replace(':', '-')}_{i}.{file_type}".replace(" ", "_")
        full_path = os.path.join(save_dir, filename)

        headers = {"Authorization": f"Bearer {jwt_token}"}
        with requests.get(download_url, headers=headers, stream=True) as r:
            if r.status_code != 200:
                results.append({
                    "status": "failed",
                    "url": download_url,
                    "error": r.text
                })
                continue

            with open(full_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            results.append({
                "status": "downloaded",
                "filename": filename,
                "path": full_path
            })

    return results