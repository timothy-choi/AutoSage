import aiohttp

async def post_instagram_story(image_url: str, access_token: str, instagram_account_id: str) -> dict:
    create_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/media"
    publish_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/stories"
    params = {
        "image_url": image_url,
        "is_stories": True,
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

async def post_video_story(video_url: str, access_token: str, instagram_account_id: str) -> dict:
    create_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/media"
    publish_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/stories"
    params = {
        "video_url": video_url,
        "media_type": "VIDEO",
        "is_stories": True,
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