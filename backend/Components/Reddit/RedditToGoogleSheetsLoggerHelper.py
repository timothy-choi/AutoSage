import requests
import gspread
from typing import Dict, Any, List
from oauth2client.service_account import ServiceAccountCredentials


class RedditToGoogleSheetsLoggerHelper:
    def __init__(self, reddit_token: str, google_creds_json: Dict[str, Any], sheet_name: str):
        self.reddit_base_url = "https://oauth.reddit.com"
        self.headers_reddit = {
            "Authorization": f"bearer {reddit_token}",
            "User-Agent": "MyApp/0.0.1"
        }

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds_json, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(sheet_name).sheet1

    def fetch_reddit_posts(self, subreddit: str, limit: int = 5) -> List[Dict[str, Any]]:
        url = f"{self.reddit_base_url}/r/{subreddit}/new?limit={limit}"
        response = requests.get(url, headers=self.headers_reddit)
        response.raise_for_status()
        return response.json()["data"]["children"]

    def log_post_to_sheet(self, post: Dict[str, Any]) -> None:
        data = post["data"]
        row = [
            data.get("id"),
            data.get("title"),
            f"https://reddit.com{data.get('permalink')}",
            data.get("author"),
            data.get("ups"),
            data.get("num_comments")
        ]
        self.sheet.append_row(row, value_input_option="USER_ENTERED")

    def log_subreddit_posts(self, subreddit: str, limit: int = 5) -> Dict[str, Any]:
        posts = self.fetch_reddit_posts(subreddit, limit)
        for post in posts:
            self.log_post_to_sheet(post)
        return {"logged_posts": len(posts)}