import requests

def generate_design_preview(file_key: str, access_token: str, node_ids: list[str] = None, format: str = "png", scale: int = 1) -> dict:
    headers = {
        "X-Figma-Token": access_token
    }

    params = {
        "format": format,
        "scale": scale
    }

    if node_ids:
        params["ids"] = ",".join(node_ids)

    url = f"https://api.figma.com/v1/images/{file_key}"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to generate preview.",
            "details": response.json()
        }

    data = response.json()
    return {
        "status": "success",
        "previews": data.get("images", {})
    }