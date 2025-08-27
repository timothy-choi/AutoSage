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


def send_posts_to_discord(discord_webhook_url, posts):
    try:
        for post in posts:
            content = (
                f"**{post['title']}**\n"
                f"🔗 [Reddit Link]({post['permalink']}) | 🌐 [Direct URL]({post['url']})\n"
                f"👤 Posted by {post['author']} | 👍 {post['score']} upvotes"
            )

            data = {"content": content}
            response = requests.post(discord_webhook_url, json=data)

            if response.status_code != 204:
                raise RuntimeError(f"Failed to send post to Discord: {response.text}")

        return {"status": "success", "message": "Posts forwarded to Discord"}

    except Exception as e:
        raise RuntimeError(f"Error sending posts to Discord: {str(e)}")