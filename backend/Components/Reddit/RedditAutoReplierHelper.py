import praw

def auto_reply_to_item(client_id, client_secret, username, password, user_agent, item_id, reply_text):
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
            raise ValueError("Invalid Reddit item ID. Must start with 't1_' (comment) or 't3_' (submission).")

        reply = item.reply(reply_text)
        return {
            "status": "success",
            "replied_to": item_id,
            "reply_id": reply.id,
            "reply_url": f"https://www.reddit.com{reply.permalink}"
        }

    except Exception as e:
        raise RuntimeError(f"Auto-reply failed: {str(e)}")