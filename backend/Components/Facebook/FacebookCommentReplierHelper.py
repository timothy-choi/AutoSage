import requests

def reply_to_comment(comment_id, message, access_token):
    url = f"https://graph.facebook.com/v18.0/{comment_id}/comments"
    payload = {
        "message": message,
        "access_token": access_token
    }
    response = requests.post(url, data=payload)
    return response.json()


def batch_reply_to_comments(comment_ids, message, access_token):
    results = {}
    for comment_id in comment_ids:
        result = reply_to_comment(comment_id, message, access_token)
        results[comment_id] = result
    return results


def keyword_reply(comment_id, comment_text, keyword_reply_map, access_token):
    for keyword, response_msg in keyword_reply_map.items():
        if keyword.lower() in comment_text.lower():
            return reply_to_comment(comment_id, response_msg, access_token)
    return {"status": "no keyword match"}


def delete_comment(comment_id, access_token):
    url = f"https://graph.facebook.com/v18.0/{comment_id}"
    params = {
        "access_token": access_token
    }
    response = requests.delete(url, params=params)
    return response.json()


def edit_comment(comment_id, new_message, access_token):
    url = f"https://graph.facebook.com/v18.0/{comment_id}"
    payload = {
        "message": new_message,
        "access_token": access_token
    }
    response = requests.post(url, data=payload)
    return response.json()