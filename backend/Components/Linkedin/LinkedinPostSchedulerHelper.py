import time
from LinkedinPostPublisherHelper import publish_linkedin_post

def schedule_linkedin_message(
    access_token: str,
    author_urn: str,
    post_text: str,
    visibility: str,
    scheduled_unix_time: int
):
    current_time = int(time.time())
    delay = scheduled_unix_time - current_time
    if delay > 0:
        time.sleep(delay)

    return publish_linkedin_post(access_token, author_urn, post_text, visibility)