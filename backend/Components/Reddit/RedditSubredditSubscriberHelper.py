import praw

def subscribe_to_subreddit(client_id, client_secret, username, password, user_agent, subreddit_name):
    """
    Subscribes the user to a given subreddit.
    """
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

        subreddit = reddit.subreddit(subreddit_name)
        subreddit.subscribe()

        return {
            "status": "success",
            "message": f"Successfully subscribed to r/{subreddit_name}"
        }

    except Exception as e:
        raise RuntimeError(f"Failed to subscribe to r/{subreddit_name}: {str(e)}")