import os
import requests
from typing import Dict, List

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def fetch_page_insights(page_id: str, metrics: List[str]) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{page_id}/insights"
    params = {
        "access_token": PAGE_ACCESS_TOKEN,
        "metric": ",".join(metrics)
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch insights: {res.status_code} - {res.text}")

    data = res.json().get("data", [])
    insights = {}
    for entry in data:
        name = entry.get("name")
        values = entry.get("values", [])
        insights[name] = values
    return insights