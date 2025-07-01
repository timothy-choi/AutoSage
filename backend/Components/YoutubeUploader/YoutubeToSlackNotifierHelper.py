import requests
from datetime import datetime, timedelta

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

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
        "maxResults": 5
    }

    response = requests.get(YOUTUBE_API_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch videos: {response.text}")

    return response.json().get("items", [])

def format_slack_blocks(videos):
    if not videos:
        return [{"type": "section", "text": {"type": "mrkdwn", "text": ":no_entry_sign: No new videos found."}}]

    blocks = [{
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*🎥 New YouTube Uploads*"}
    }]

    for video in videos:
        vid_id = video["id"]["videoId"]
        snippet = video["snippet"]
        title = snippet["title"]
        url = f"https://www.youtube.com/watch?v={vid_id}"
        published = snippet.get("publishedAt", "")
        description = snippet.get("description", "")[:100]

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*<{url}|{title}>*\n{description}\n📅 {published}"
            }
        })
        blocks.append({"type": "divider"})

    return blocks

def send_to_slack(slack_webhook_url, blocks):
    response = requests.post(slack_webhook_url, json={"blocks": blocks})
    return {
        "status": response.status_code,
        "success": response.status_code == 200,
        "detail": response.text if response.status_code != 200 else "Posted successfully"
    }

def notify_youtube_uploads_to_slack(api_key, channel_id, slack_webhook_url, published_within_minutes=60):
    videos = fetch_recent_youtube_videos(api_key, channel_id, published_within_minutes)
    blocks = format_slack_blocks(videos)
    return send_to_slack(slack_webhook_url, blocks)