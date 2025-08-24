import praw

def edit_reddit_comment(client_id, client_secret, username, password, user_agent, comment_id, new_text):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    try:
        comment = reddit.comment(id=comment_id)
        comment_author = comment.author.name if comment.author else None

        if comment_author != username:
            raise PermissionError("You can only edit your own comment.")

        comment.edit(new_text)

        return {
            "status": "edited",
            "comment_id": comment_id,
            "new_text": new_text
        }

    except Exception as e:
        raise RuntimeError(f"Error editing comment: {str(e)}")