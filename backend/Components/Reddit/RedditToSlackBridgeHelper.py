import praw
import requests

def fetch_latest_posts(client_id, client_secret, username, password, user_agent, subreddit_name, limit=5):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

        subreddit = reddit.subreddit(subreddit_name)
        posts = []

        for submission in subreddit.new(limit=limit):
            posts.append({
                "title": submission.title,
                "url": submission.url,
                "permalink": f"https://reddit.com{submission.permalink}",
                "author": str(submission.author),
                "score": submission.score
            })

        return posts

    except Exception as e:
        raise RuntimeError(f"Failed to fetch posts from r/{subreddit_name}: {str(e)}")


def send_posts_to_slack(slack_webhook_url, posts):
    try:
        for post in posts:
            text = (
                f"*{post['title']}*\n"
                f"<{post['permalink']}|Reddit Link> | "
                f"<{post['url']}|Direct URL>\n"
                f"_Posted by u/{post['author']} | {post['score']} upvotes_"
            )

            payload = {"text": text}
            response = requests.post(slack_webhook_url, json=payload)

            if response.status_code != 200:
                raise RuntimeError(f"Failed to send post to Slack: {response.text}")

        return {"status": "success", "message": "Posts forwarded to Slack"}

    except Exception as e:
        raise RuntimeError(f"Error sending posts to Slack: {str(e)}")