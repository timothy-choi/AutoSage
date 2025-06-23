import os
import requests
import tweepy

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def format_linkedin_post_for_tweet(content: str, max_length: int = 280) -> str:
    text = content.strip().replace('\n\n', '\n')
    return text[:max_length]

def post_to_twitter(content: str) -> dict:
    try:
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY, TWITTER_API_SECRET,
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)
        tweet = api.update_status(status=content)
        return {"status": "success", "tweet_id": tweet.id, "link": f"https://x.com/user/status/{tweet.id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def forward_linkedin_post_to_twitter(linkedin_post: str) -> dict:
    formatted = format_linkedin_post_for_tweet(linkedin_post)
    return post_to_twitter(formatted)