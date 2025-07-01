import requests
from datetime import datetime, timedelta

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
TWITTER_API_URL = "https://api.twitter.com/2/tweets"

def fetch_recent_youtube_videos(api_key, channel_id, published_within_minutes=60):
    now = datetime.utcnow()
    published_after = (now - timedelta(minutes=published_within_minutes)).isoformat("T") + "Z"

    params = {
        "key": api_key,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "type": "video",
        "publishedAfter": published_after,
        "maxResults": 3
    }

    response = requests.get(YOUTUBE_API_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch videos: {response.text}")

    return response.json().get("items", [])

def create_tweet_from_video(video):
    snippet = video["snippet"]
    title = snippet["title"]
    video_id = video["id"]["videoId"]
    url = f"https://youtu.be/{video_id}"
    hashtags = "#YouTube #NewVideo"

    tweet = f"🎬 {title}\n\nWatch now: {url}\n\n{hashtags}"
    return tweet

def post_tweet(tweet_text, twitter_bearer_token):
    headers = {
        "Authorization": f"Bearer {twitter_bearer_token}",
        "Content-Type": "application/json"
    }
    payload = {"text": tweet_text}

    response = requests.post(TWITTER_API_URL, json=payload, headers=headers)
    return {
        "status": response.status_code,
        "tweet_id": response.json().get("data", {}).get("id"),
        "error": response.text if response.status_code != 201 else None
    }

def sync_youtube_to_twitter(api_key, channel_id, twitter_token, published_within_minutes=60):
    videos = fetch_recent_youtube_videos(api_key, channel_id, published_within_minutes)
    results = []

    for video in videos:
        tweet = create_tweet_from_video(video)
        result = post_tweet(tweet, twitter_token)
        result["video_title"] = video["snippet"]["title"]