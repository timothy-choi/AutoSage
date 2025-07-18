import requests

def export_figma_frames(file_key: str, frame_ids: list[str], access_token: str, format: str = "png", scale: int = 1) -> dict:
    headers = {
        "X-Figma-Token": access_token
    }

    ids_param = ",".join(frame_ids)
    params = {
        "ids": ids_param,
        "format": format,
        "scale": scale
    }

    export_url = f"https://api.figma.com/v1/images/{file_key}"
    response = requests.get(export_url, headers=headers, params=params)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to export frames: {response.status_code}",
            "details": response.json()
        }

    data = response.json()
    return {
        "status": "success",
        "images": data.get("images", {})
    }