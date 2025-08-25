import praw

def downvote_item(client_id, client_secret, username, password, user_agent, item_id):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

        if item_id.startswith("t1_"):
            item = reddit.comment(item_id[3:])
        elif item_id.startswith("t3_"):
            item = reddit.submission(item_id[3:])
        else:
            raise ValueError("Invalid Reddit item ID. Must start with 't1_' or 't3_'.")

        item.downvote()
        return {"status": "success", "item_id": item_id}
    except Exception as e:
        raise RuntimeError(f"Downvote failed: {str(e)}")