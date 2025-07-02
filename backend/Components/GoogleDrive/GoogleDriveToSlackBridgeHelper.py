import requests

def send_drive_files_to_slack(files: list, slack_webhook_url: str) -> dict:
    if not files:
        return {"status": "skipped", "message": "No files to send"}

    for file in files:
        name = file.get("name", "Unknown file")
        link = file.get("webViewLink", "No link")
        mime = file.get("mimeType", "Unknown type")
        size = int(file.get("size", 0)) / (1024 * 1024)
        size_str = f"{size:.2f} MB" if size else "Unknown size"

        payload = {
            "text": f"📄 *New Google Drive File Detected:*\n"
                    f"*Name:* {name}\n"
                    f"*Type:* {mime}\n"
                    f"*Size:* {size_str}\n"
                    f"*Link:* {link}"
        }

        response = requests.post(slack_webhook_url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Slack webhook failed: {response.text}")

    return {"status": "success", "message": f"{len(files)} file(s) sent to Slack"}