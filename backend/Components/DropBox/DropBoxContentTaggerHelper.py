import requests
from typing import List
from io import BytesIO
from PyPDF2 import PdfReader
import openai  

DROPBOX_DOWNLOAD_URL = "https://content.dropboxapi.com/2/files/download"

def download_file(access_token: str, path: str) -> bytes:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Dropbox-API-Arg": f'{{"path": "{path}"}}'
    }
    res = requests.post(DROPBOX_DOWNLOAD_URL, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Dropbox download failed: {res.text}")
    return res.content

def extract_text(file_path: str, file_bytes: bytes) -> str:
    if file_path.endswith((".txt", ".md")):
        return file_bytes.decode("utf-8", errors="ignore")
    elif file_path.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    else:
        raise Exception("Unsupported file type for tagging")

def extract_tags_with_ai(text: str, max_tags: int = 10) -> List[str]:
    openai.api_key = "your-openai-api-key"  
    prompt = f"""Extract up to {max_tags} relevant topic or keyword tags from this document. Return as a JSON list.
    
{text[:4000]}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response.choices[0].message.content.strip()

    try:
        tags = eval(content)
        return [tag.strip() for tag in tags if isinstance(tag, str)]
    except:
        return ["Tag parsing failed"]

def tag_dropbox_file(access_token: str, path: str) -> dict:
    file_bytes = download_file(access_token, path)
    text = extract_text(path, file_bytes)
    tags = extract_tags_with_ai(text)
    return {
        "path": path,
        "tags": tags
    }