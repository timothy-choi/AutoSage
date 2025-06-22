import os
import re
import requests
from typing import List, Dict

ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def search_facebook_pages(query: str, limit: int = 1) -> List[Dict]:
    url = f"https://graph.facebook.com/v17.0/search"
    params = {
        "access_token": ACCESS_TOKEN,
        "q": query,
        "type": "page",
        "limit": limit
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get("data", [])
    return []

def extract_entities_to_tag(text: str) -> List[Dict]:
    words = list(set(re.findall(r'\b[a-zA-Z][a-zA-Z ]{2,}\b', text.lower())))
    found = []

    for word in words:
        results = search_facebook_pages(word)
        if results:
            page = results[0]
            found.append({
                "name": word,
                "entity_id": page["id"],
                "entity_name": page["name"],
                "entity_link": f"https://www.facebook.com/{page['id']}"
            })
    return found

def inject_links_into_text(text: str, entities: List[Dict]) -> str:
    for entity in entities:
        pattern = re.compile(fr'\b{re.escape(entity["name"])}\b', re.IGNORECASE)
        replacement = f"[{entity['entity_name']}]({entity['entity_link']})"
        text = pattern.sub(replacement, text, count=1)
    return text