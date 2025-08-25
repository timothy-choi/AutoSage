import praw
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

def submit_post(client_id, client_secret, username, password, user_agent, subreddit, title, body):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    try:
        subreddit_ref = reddit.subreddit(subreddit)
        post = subreddit_ref.submit(title=title, selftext=body)
        return {"status": "posted", "url": post.url, "post_id": post.id}
    except Exception as e:
        raise RuntimeError(f"Failed to post: {str(e)}")

def schedule_post(client_id, client_secret, username, password, user_agent, subreddit, title, body, scheduled_time):
    job = scheduler.add_job(
        submit_post,
        'date',
        run_date=scheduled_time,
        args=[client_id, client_secret, username, password, user_agent, subreddit, title, body]
    )
    return {"status": "scheduled", "job_id": job.id, "run_time": str(scheduled_time)}