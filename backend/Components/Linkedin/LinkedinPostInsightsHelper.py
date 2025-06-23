import requests

def fetch_linkedin_post_insights(access_token: str, post_urn: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    post_id = post_urn.split(":")[-1]
    url = f"https://api.linkedin.com/v2/socialActions/urn:li:ugcPost:{post_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return {
            "likes": data.get("likesSummary", {}).get("totalLikes", 0),
            "comments": data.get("commentsSummary", {}).get("count", 0),
            "shares": data.get("shareStatistics", {}).get("shareCount", 0),
            "insights_raw": data
        }
    except requests.exceptions.HTTPError as e:
        return {"error": response.json()}
    except Exception as e:
        return {"error": str(e)}