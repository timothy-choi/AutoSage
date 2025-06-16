import aiohttp

async def reply_to_comment(comment_id: str, message: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"
    payload = {
        "message": message,
        "access_token": access_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            if resp.status not in [200, 201]:
                return {"error": f"Failed to reply: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "replied", "comment_id": comment_id}

async def like_comment(comment_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{comment_id}/likes"
    payload = {"access_token": access_token}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            if resp.status not in [200, 201]:
                return {"error": f"Failed to like comment: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "liked", "comment_id": comment_id}

async def delete_comment(comment_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{comment_id}"
    params = {"access_token": access_token}
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, params=params) as resp:
            if resp.status != 200:
                return {"error": f"Failed to delete comment: HTTP {resp.status}", "details": await resp.text()}
            return {"status": "deleted", "comment_id": comment_id}