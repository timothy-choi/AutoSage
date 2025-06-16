import os
import aiohttp
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.start()

scheduled_posts = []

async def schedule_instagram_post(image_url: str, caption: str, post_time: str, access_token: str, instagram_account_id: str) -> dict:
    post_time_obj = datetime.fromisoformat(post_time)
    scheduled_posts.append({"image_url": image_url, "caption": caption, "post_time": post_time_obj})
    scheduler.add_job(
        post_to_instagram,
        trigger='date',
        run_date=post_time_obj,
        args=[image_url, caption, access_token, instagram_account_id]
    )
    return {"status": "scheduled", "post_time": post_time}

async def post_to_instagram(image_url: str, caption: str, access_token: str, instagram_account_id: str):
    create_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/media"
    publish_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/media_publish"
    params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(create_url, params=params) as create_resp:
            create_data = await create_resp.json()
            creation_id = create_data.get("id")
            if not creation_id:
                return {"error": create_data}
            publish_params = {
                "creation_id": creation_id,
                "access_token": access_token
            }
            async with session.post(publish_url, params=publish_params) as publish_resp:
                publish_data = await publish_resp.json()
                return publish_data