import requests

def send_drive_files_to_discord(
    files: list,
    discord_webhook_url: str
) -> dict:
    if not files:
        return {"status": "skipped", "message": "No files to send"}

    for file in files:
        name = file.get("name", "Unnamed file")
        link = file.get("webViewLink", "")
        mime = file.get("mimeType", "Unknown type")
        size = int(file.get("size", 0)) / (1024 * 1024)
        size_str = f"{size:.2f} MB" if size else "Unknown size"

        content = (
            f"📄 **New Google Drive File**\n"
            f"**Name:** {name}\n"
            f"**Type:** {mime}\n"
            f"**Size:** {size_str}\n"
            f"**Link:** [View File]({link})"
        )

        response = requests.post(discord_webhook_url, json={"content": content})
        if response.status_code != 204:
            raise Exception(f"Discord webhook failed: {response.text}")

    return {"status": "success", "message": f"{len(files)} file(s) sent to Discord"}