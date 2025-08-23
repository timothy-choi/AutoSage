import praw

def create_reddit_post(client_id, client_secret, username, password, user_agent, subreddit, title, body=None, url=None):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    subreddit_obj = reddit.subreddit(subreddit)

    if url:
        post = subreddit_obj.submit(title=title, url=url)
    else:
        post = subreddit_obj.submit(title=title, selftext=body or "")

    return {
        "id": post.id,
        "title": post.title,
        "url": post.url,
        "permalink": f"https://reddit.com{post.permalink}"
    }