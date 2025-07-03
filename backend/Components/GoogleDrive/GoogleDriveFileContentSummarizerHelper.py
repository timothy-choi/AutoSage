import requests
import openai

DRIVE_API_URL = "https://www.googleapis.com/drive/v3/files/{file_id}/export"
DRIVE_DOWNLOAD_URL = "https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

def download_file_content(
    access_token: str,
    file_id: str,
    mime_type: str
) -> str:
    headers = {"Authorization": f"Bearer {access_token}"}

    if mime_type == "application/vnd.google-apps.document":
        response = requests.get(
            DRIVE_API_URL.format(file_id=file_id),
            headers=headers,
            params={"mimeType": "text/plain"}
        )
    else:
        response = requests.get(
            DRIVE_DOWNLOAD_URL.format(file_id=file_id),
            headers=headers
        )

    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.text}")

    text = response.text
    if len(text) > 6000:  
        text = text[:6000]
    return text

def summarize_text_with_ai(
    text: str,
    openai_api_key: str,
    max_tokens: int = 150
) -> str:
    openai.api_key = openai_api_key

    prompt = (
        "Summarize the following document into a concise paragraph highlighting the key points:\n\n"
        f"{text}\n\nSummary:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.3
    )

    summary = response.choices[0].message.content.strip()
    return summary

def summarize_drive_file_with_ai(
    access_token: str,
    file_id: str,
    mime_type: str,
    openai_api_key: str
) -> dict:
    content = download_file_content(access_token, file_id, mime_type)
    summary = summarize_text_with_ai(content, openai_api_key)

    return {
        "status": "success",
        "file_id": file_id,
        "summary": summary
    }