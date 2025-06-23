import requests

def publish_linkedin_post(access_token: str, author_urn: str, post_text: str, visibility: str = "PUBLIC"):
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": visibility
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {"status": "success", "post_urn": response.json().get("id")}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "details": response.json()}
    except Exception as e:
        return {"status": "error", "details": str(e)}