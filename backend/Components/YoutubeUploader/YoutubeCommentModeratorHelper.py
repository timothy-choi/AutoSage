import requests

YOUTUBE_COMMENTS_API = "https://www.googleapis.com/youtube/v3/commentThreads"
YOUTUBE_DELETE_COMMENT_API = "https://www.googleapis.com/youtube/v3/comments"

def fetch_video_comments(api_key, video_id, max_results=100):
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "textFormat": "plainText",
        "key": api_key
    }
    response = requests.get(YOUTUBE_COMMENTS_API, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch comments: {response.text}")

    return response.json().get("items", [])

def moderate_comments(comments, banned_keywords):
    flagged = []

    for comment_thread in comments:
        comment = comment_thread["snippet"]["topLevelComment"]["snippet"]
        comment_id = comment_thread["snippet"]["topLevelComment"]["id"]
        text = comment.get("textDisplay", "").lower()

        if any(bad_word.lower() in text for bad_word in banned_keywords):
            flagged.append({
                "id": comment_id,
                "text": comment.get("textDisplay"),
                "author": comment.get("authorDisplayName")
            })

    return flagged

def delete_youtube_comment(api_key, comment_id):
    url = f"{YOUTUBE_DELETE_COMMENT_API}?id={comment_id}&key={api_key}"
    response = requests.delete(url)
    return {
        "comment_id": comment_id,
        "status": response.status_code,
        "result": "deleted" if response.status_code == 204 else response.text
    }

def moderate_and_optionally_delete(api_key, video_id, banned_keywords, delete_flag=False):
    comments = fetch_video_comments(api_key, video_id)
    flagged = moderate_comments(comments, banned_keywords)

    results = []
    for item in flagged:
        result = {"comment": item}
        if delete_flag:
            deletion = delete_youtube_comment(api_key, item["id"])
            result["deletion"] = deletion
        results.append(result)

    return results