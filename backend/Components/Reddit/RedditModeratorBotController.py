from fastapi import APIRouter, Query
from typing import List
from RedditModeratorBotHelper import RedditModeratorBotHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str, subreddit: str) -> RedditModeratorBotHelper:
    key = f"{subreddit}:{token}"
    if key not in helper_instances:
        helper_instances[key] = RedditModeratorBotHelper(token, subreddit)
    return helper_instances[key]

@router.get("/moderator/fetch")
def fetch_new_posts(token: str, subreddit: str, limit: int = 10):
    helper = get_helper(token, subreddit)
    return helper.fetch_new_content(limit=limit)

@router.post("/moderator/remove")
def remove_post(token: str, subreddit: str, post_id: str, reason: str = "Rule violation"):
    helper = get_helper(token, subreddit)
    return helper.remove_post(post_id, reason)

@router.post("/moderator/approve")
def approve_post(token: str, subreddit: str, post_id: str):
    helper = get_helper(token, subreddit)
    return helper.approve_post(post_id)

@router.post("/moderator/flag")
def flag_post(token: str, subreddit: str, post_id: str, reason: str = "Needs review"):
    helper = get_helper(token, subreddit)
    return helper.flag_post(post_id, reason)

@router.post("/moderator/auto")
def auto_moderate(
    token: str,
    subreddit: str,
    banned_keywords: List[str] = Query(default=["spam", "scam"]),
    limit: int = 10
):
    helper = get_helper(token, subreddit)
    posts = helper.fetch_new_content(limit=limit)
    return helper.auto_moderate(posts, banned_keywords)