import praw

def upvote_item(client_id, client_secret, username, password, user_agent, item_id):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

        item = reddit.comment(item_id) if item_id.startswith("t1_") else reddit.submission(item_id)
        item.upvote()
        return {"status": "success", "item_id": item_id}
    except Exception as e:
        raise RuntimeError(f"Upvote failed: {str(e)}")