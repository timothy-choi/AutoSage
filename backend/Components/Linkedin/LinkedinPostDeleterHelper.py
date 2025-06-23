import requests

def delete_linkedin_post(access_token: str, post_urn: str):
    post_id = post_urn.split(":")[-1]
    url = f"https://api.linkedin.com/v2/ugcPosts/{post_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return {"status": "success", "message": f"Post {post_urn} deleted successfully."}
        else:
            return {
                "status": "error",
                "message": f"Failed to delete post {post_urn}",
                "details": response.json()
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}