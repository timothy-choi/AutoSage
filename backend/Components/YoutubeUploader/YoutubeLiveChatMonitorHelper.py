from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_live_chat_id(access_token: str) -> str:
    credentials = Credentials(token=access_token)
    youtube = build("youtube", "v3", credentials=credentials)

    broadcasts = youtube.liveBroadcasts().list(
        part="snippet",
        broadcastStatus="active",
        mine=True
    ).execute()

    items = broadcasts.get("items", [])
    if not items:
        raise RuntimeError("No active broadcast found.")

    return items[0]["snippet"]["liveChatId"]

def fetch_live_chat_messages(access_token: str, live_chat_id: str, max_results: int = 10) -> list[dict]:
    credentials = Credentials(token=access_token)
    youtube = build("youtube", "v3", credentials=credentials)

    response = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet,authorDetails",
        maxResults=max_results
    ).execute()

    messages = []
    for item in response.get("items", []):
        msg = item["snippet"]["displayMessage"]
        author = item["authorDetails"]["displayName"]
        time_sent = item["snippet"]["publishedAt"]
        messages.append({
            "author": author,
            "message": msg,
            "timestamp": time_sent
        })

    return messages

def monitor_live_chat_once(access_token: str, max_results: int = 10) -> dict:
    try:
        live_chat_id = get_live_chat_id(access_token)
        messages = fetch_live_chat_messages(access_token, live_chat_id, max_results)
        return {
            "status": "success",
            "chat_id": live_chat_id,
            "messages": messages
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }