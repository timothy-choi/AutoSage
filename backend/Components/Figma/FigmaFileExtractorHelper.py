import requests

def extract_figma_styles(file_key: str, access_token: str) -> dict:
    headers = {
        "X-Figma-Token": access_token
    }

    file_url = f"https://api.figma.com/v1/files/{file_key}"
    response = requests.get(file_url, headers=headers)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to fetch Figma file: {response.status_code}",
            "details": response.json()
        }

    data = response.json()
    styles = {
        "textStyles": {},
        "colorStyles": {},
        "effectStyles": {}
    }

    if "styles" in data:
        for style_id, style in data["styles"].items():
            style_type = style.get("style_type")
            if style_type == "TEXT":
                styles["textStyles"][style_id] = style
            elif style_type == "FILL":
                styles["colorStyles"][style_id] = style
            elif style_type == "EFFECT":
                styles["effectStyles"][style_id] = style

    return {
        "status": "success",
        "styles": styles
    }