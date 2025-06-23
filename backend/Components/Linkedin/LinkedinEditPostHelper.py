from LinkedinPostDeleterHelper import delete_linkedin_post
from LinkedinPostPublisherHelper import publish_linkedin_post

def edit_linkedin_post(access_token: str, post_urn: str, author_urn: str, new_content: str, visibility: str = "PUBLIC"):
    delete_result = delete_linkedin_post(access_token, post_urn)
    if delete_result.get("status") != "success":
        return {"status": "error", "step": "delete", "details": delete_result}

    publish_result = publish_linkedin_post(access_token, author_urn, new_content, visibility)
    if publish_result.get("status") != "success":
        return {"status": "error", "step": "repost", "details": publish_result}

    return {
        "status": "success",
        "message": f"Post edited successfully. New post URN: {publish_result.get('post_urn')}"
    }