import requests
from typing import Dict, List
import openai

NOTION_VERSION = "2022-06-28"
NOTION_PAGE_URL = "https://api.notion.com/v1/pages/{}"
NOTION_BLOCKS_URL = "https://api.notion.com/v1/blocks/{}/children"

def fetch_page_blocks(notion_token: str, page_id: str, max_blocks: int = 100) -> List[str]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION
    }

    url = NOTION_BLOCKS_URL.format(page_id)
    response = requests.get(url, headers=headers, params={"page_size": max_blocks})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch blocks: {response.text}")

    blocks = response.json().get("results", [])
    texts = []
    for block in blocks:
        block_type = block.get("type", "")
        rich_text = block.get(block_type, {}).get("rich_text", [])
        for rt in rich_text:
            texts.append(rt.get("plain_text", ""))
    return texts

def summarize_with_openai(api_key: str, content: List[str]) -> str:
    openai.api_key = api_key
    prompt = "Summarize the following notes:\n\n" + "\n".join(content[:100])
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.5
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error during summarization: {str(e)}"

def generate_notion_summary(notion_token: str, page_id: str, openai_api_key: str) -> Dict:
    try:
        content = fetch_page_blocks(notion_token, page_id)
        if not content:
            return {"summary": "No content found on the page."}
        summary = summarize_with_openai(openai_api_key, content)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}