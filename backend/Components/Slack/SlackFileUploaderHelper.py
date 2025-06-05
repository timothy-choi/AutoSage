import requests

def upload_slack_file(token: str, channel: str, file_path: str, title: str = None) -> dict:
    with open(file_path, "rb") as file_content:
        response = requests.post(
            "https://slack.com/api/files.upload",
            headers={"Authorization": f"Bearer {token}"},
            data={
                "channels": channel,
                "title": title or file_path
            },
            files={"file": file_content}
        )
    return response.json()