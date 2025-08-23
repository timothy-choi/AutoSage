import praw

def delete_reddit_post(client_id, client_secret, username, password, user_agent, post_id):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    submission = reddit.submission(id=post_id)
    submission.delete()

    return {
        "status": "deleted",
        "post_id": post_id
    }