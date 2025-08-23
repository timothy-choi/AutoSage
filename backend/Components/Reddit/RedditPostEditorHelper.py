import praw

def edit_reddit_post(client_id, client_secret, username, password, user_agent, post_id, new_text):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent,
    )

    submission = reddit.submission(id=post_id)
    
    if submission.is_self:
        submission.edit(new_text)
        return {
            "status": "edited",
            "post_id": post_id,
            "new_text": new_text
        }
    else:
        raise ValueError("Only text (self) posts can be edited.")