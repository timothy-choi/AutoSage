import requests
from typing import Dict, Any

class RedditToNotionSyncerHelper:
    def __init__(self, reddit_token: str, notion_token: str, notion_db_id: str):
        self.reddit_base_url = "https://oauth.reddit.com"
        self.headers_reddit = {"Authorization": f"bearer {reddit_token}", "User-Agent": "MyApp/0.0.1"}
        self.headers_notion = {"Authorization": f"Bearer {notion_token}", "Notion-Version": "2022-06-28"}
        self.notion_db_id = notion_db_id
        self.notion_base_url = "https://api.notion.com/v1"

    def fetch_reddit_posts(self, subreddit: str, limit: int = 5) -> Dict[str, Any]:
        url = f"{self.reddit_base_url}/r/{subreddit}/new?limit={limit}"
        response = requests.get(url, headers=self.headers_reddit)
        response.raise_for_status()
        return response.json()

    def sync_post_to_notion(self, post: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.notion_base_url}/pages"
        data = {
            "parent": {"database_id": self.notion_db_id},
            "properties": {
                "Title": {"title": [{"text": {"content": post['data']['title']}}]},
                "URL": {"url": f"https://reddit.com{post['data']['permalink']}"},
                "Upvotes": {"number": post['data']['ups']}
            }
        }
        response = requests.post(url, headers=self.headers_notion, json=data)
        response.raise_for_status()
        return response.json()

    def sync_subreddit_posts(self, subreddit: str, limit: int = 5) -> Dict[str, Any]:
        posts_data = self.fetch_reddit_posts(subreddit, limit)
        synced = []
        for post in posts_data["data"]["children"]:
            synced_post = self.sync_post_to_notion(post)
            synced.append(synced_post)
        return {"synced_posts": synced}