import requests
from typing import Dict, Any, List


class RedditModeratorBotHelper:
    def __init__(self, reddit_token: str, subreddit: str):
        self.base_url = "https://oauth.reddit.com"
        self.headers = {
            "Authorization": f"bearer {reddit_token}",
            "User-Agent": "RedditModeratorBot/0.0.1"
        }
        self.subreddit = subreddit

    def fetch_new_content(self, limit: int = 10) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/r/{self.subreddit}"
        resp = requests.get(url, headers=self.headers, params={"limit": limit})
        if resp.status_code == 200:
            data = resp.json()
            return data.get("data", {}).get("children", [])
        return []

    def remove_post(self, post_id: str, reason: str = "Rule violation") -> Dict[str, Any]:
        url = f"{self.base_url}/api/remove"
        resp = requests.post(url, headers=self.headers, data={"id": post_id})
        return {"status": resp.status_code, "action": "removed", "reason": reason}

    def approve_post(self, post_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/approve"
        resp = requests.post(url, headers=self.headers, data={"id": post_id})
        return {"status": resp.status_code, "action": "approved"}

    def flag_post(self, post_id: str, reason: str = "Needs review") -> Dict[str, Any]:
        return {"status": "flagged", "post_id": post_id, "reason": reason}

    def auto_moderate(self, posts: List[Dict[str, Any]], banned_keywords: List[str]) -> List[Dict[str, Any]]:
        actions = []
        for post in posts:
            post_id = post["data"]["name"]
            title = post["data"]["title"].lower()
            if any(bad_word in title for bad_word in banned_keywords):
                actions.append(self.remove_post(post_id, reason="Banned keyword"))
            else:
                actions.append(self.approve_post(post_id))
        return actions