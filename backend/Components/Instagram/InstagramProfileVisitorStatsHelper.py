import aiohttp

async def get_profile_visits(instagram_account_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/insights?metric=profile_views&period=day&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch profile visitor stats: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()
            return data

async def get_profile_reach(instagram_account_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/insights?metric=reach&period=day&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch reach data: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()
            return data

async def get_profile_impressions(instagram_account_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/insights?metric=impressions&period=day&access_token={access_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch impressions data: HTTP {resp.status}", "details": await resp.text()}
            data = await resp.json()
            return data