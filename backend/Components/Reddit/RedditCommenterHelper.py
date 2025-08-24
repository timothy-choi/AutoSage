import praw

def comment_on_reddit(client_id, client_secret, username, password, user_agent, target_id, text):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent,
    )

    if target_id.startswith("t3_"):
        submission = reddit.submission(id=target_id[3:])
        comment = submission.reply(text)
    elif target_id.startswith("t1_"):
        parent_comment = reddit.comment(id=target_id[3:])
        comment = parent_comment.reply(text)
    else:
        raise ValueError("Invalid target_id. Must start with 't3_' for submissions or 't1_' for comments.")

    return {
        "status": "commented",
        "comment_id": comment.id,
        "parent_id": target_id,
        "text": text,
        "permalink": f"https://www.reddit.com{comment.permalink}"
    }