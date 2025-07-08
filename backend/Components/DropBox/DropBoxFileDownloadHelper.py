import requests

DROPBOX_DOWNLOAD_URL = "https://content.dropboxapi.com/2/files/download"

def download_file_from_dropbox(
    access_token: str,
    dropbox_file_path: str,
    local_dest_path: str
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Dropbox-API-Arg": str({
            "path": dropbox_file_path
        }).replace("'", '"')
    }

    response = requests.post(DROPBOX_DOWNLOAD_URL, headers=headers, stream=True)

    if response.status_code != 200:
        raise Exception(f"Dropbox download failed: {response.text}")

    with open(local_dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)

    return {
        "status": "success",
        "dropbox_path": dropbox_file_path,
        "local_path": local_dest_path,
        "size_bytes": int(response.headers.get("Content-Length", 0))
    }