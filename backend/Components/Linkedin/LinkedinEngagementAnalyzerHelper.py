import requests
from typing import Literal

def fetch_linkedin_posts(access_token: str, entity_urn: str, entity_type: Literal["user", "organization"] = "user", count: int = 10):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    url = f"https://api.linkedin.com/v2/ugcPosts"
    params = {
        "q": "authors",
        "authors": f"List({entity_urn})",
        "sortBy": "LAST_MODIFIED",
        "count": count
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        posts_raw = response.json().get("elements", [])

        posts = []
        for post in posts_raw:
            post_data = {
                "content": post.get("specificContent", {}).get("com.linkedin.ugc.ShareContent", {}).get("shareCommentary", {}).get("text", ""),
                "likes": 0,        
                "comments": 0,
                "shares": 0,
                "impressions": 0
            }
            posts.append(post_data)

        return posts
    except Exception as e:
        return {"error": f"Failed to fetch posts: {e}"}

def analyze_linkedin_engagement(posts: list[dict]) -> dict:
    if not posts:
        return {"error": "No posts provided."}

    total_likes = total_comments = total_shares = total_impressions = 0
    top_post = None
    max_engagement = -1

    for post in posts:
        likes = post.get("likes", 0)
        comments = post.get("comments", 0)
        shares = post.get("shares", 0)
        impressions = post.get("impressions", 0)

        total_likes += likes
        total_comments += comments
        total_shares += shares
        total_impressions += impressions

        engagement = likes + comments + shares
        if engagement > max_engagement:
            max_engagement = engagement
            top_post = post

    total_posts = len(posts)
    avg_likes = total_likes / total_posts
    avg_comments = total_comments / total_posts
    avg_shares = total_shares / total_posts
    engagement_rate = (total_likes + total_comments + total_shares) / total_impressions if total_impressions > 0 else None

    return {
        "total_posts": total_posts,
        "average_likes": round(avg_likes, 2),
        "average_comments": round(avg_comments, 2),
        "average_shares": round(avg_shares, 2),
        "engagement_rate": round(engagement_rate * 100, 2) if engagement_rate else None,
        "top_post": top_post
    }