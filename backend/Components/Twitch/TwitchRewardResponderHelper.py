import aiohttp

async def respond_to_channel_point_reward(oauth_token: str, client_id: str, reward_id: str, user_input: str, message: str) -> dict:
    url = f"https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions"
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }
    params = {
        "broadcaster_id": client_id,
        "reward_id": reward_id,
        "status": "UNFULFILLED"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch redemptions: HTTP {resp.status}"}
            data = await resp.json()

    matched = [r for r in data.get("data", []) if r.get("user_input") == user_input]
    if not matched:
        return {"error": "No matching redemption found for user input."}

    redemption_id = matched[0]["id"]
    patch_url = f"{url}?id={redemption_id}&broadcaster_id={client_id}&reward_id={reward_id}"
    payload = {"status": "FULFILLED"}

    async with aiohttp.ClientSession() as session:
        async with session.patch(patch_url, headers=headers, json=payload) as patch_resp:
            if patch_resp.status not in [200, 204]:
                return {"error": f"Failed to fulfill reward: HTTP {patch_resp.status}"}

    return {"status": "Reward fulfilled", "message": message}