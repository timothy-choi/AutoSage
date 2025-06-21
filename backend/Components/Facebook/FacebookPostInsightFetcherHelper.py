import os
import requests
from typing import Dict

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

POST_METRICS = [
    "post_impressions",
    "post_impressions_unique",
    "post_engaged_users",
    "post_clicks",
    "post_reactions_by_type_total"
]

def fetch_post_insights(post_id: str) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{post_id}/insights"
    res = requests.get(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "metric": ",".join(POST_METRICS)
    })

    if res.status_code == 200:
        metrics = res.json().get("data", [])
        return {metric["name"]: metric.get("values", [{}])[0].get("value") for metric in metrics}
    else:
        raise Exception(f"Failed to fetch insights: {res.status_code} - {res.text}")