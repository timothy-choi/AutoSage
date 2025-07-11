import requests
from typing import Optional
from PyPDF2 import PdfReader
from io import BytesIO
import openai

DROPBOX_DOWNLOAD_URL = "https://content.dropboxapi.com/2/files/download"

def download_file_from_dropbox(access_token: str, path: str) -> bytes:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Dropbox-API-Arg": f'{{"path": "{path}"}}'
    }
    response = requests.post(DROPBOX_DOWNLOAD_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"File download failed: {response.text}")
    return response.content

def extract_text_from_file(path: str, file_bytes: bytes) -> str:
    if path.endswith(".txt") or path.endswith(".md"):
        return file_bytes.decode("utf-8", errors="ignore")
    elif path.endswith(".pdf"):
        pdf = PdfReader(BytesIO(file_bytes))
        return "\n".join([page.extract_text() or "" for page in pdf.pages])
    else:
        raise Exception("Unsupported file type for summarization")

def summarize_text_ai(text: str, max_words: int = 150) -> str:
    openai.api_key = "your-openai-api-key"  

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You summarize text documents."},
            {"role": "user", "content": f"Summarize this in under {max_words} words:\n{text}"}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def summarize_dropbox_file(access_token: str, path: str) -> dict:
    raw_data = download_file_from_dropbox(access_token, path)
    extracted_text = extract_text_from_file(path, raw_data)

    if not extracted_text.strip():
        raise Exception("No readable text found in file.")

    summary = summarize_text_ai(extracted_text)

    return {
        "path": path,
        "summary": summary
    }