import praw

def delete_reddit_comment(client_id, client_secret, username, password, user_agent, comment_id):
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
            raise PermissionError("You can only delete your own comment.")

        comment.delete()

        return {
            "status": "deleted",
            "comment_id": comment_id
        }

    except Exception as e:
        raise RuntimeError(f"Error deleting comment: {str(e)}")