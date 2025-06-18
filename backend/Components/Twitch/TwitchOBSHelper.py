import aiohttp

OBS_WEBSOCKET_URL = "http://localhost:4455"
OBS_PASSWORD = "your_obs_password"

async def send_obs_command(command: str, params: dict = {}) -> dict:
    payload = {
        "op": 6,  # Request
        "d": {
            "requestType": command,
            "requestId": "cmd_" + command,
            "requestData": params
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OBS_WEBSOCKET_URL, json=payload, headers=headers, auth=aiohttp.BasicAuth("", OBS_PASSWORD)) as resp:
            if resp.status != 200:
                return {"error": f"OBS command failed: HTTP {resp.status}", "details": await resp.text()}
            return await resp.json()


async def start_streaming() -> dict:
    return await send_obs_command("StartStream")

async def stop_streaming() -> dict:
    return await send_obs_command("StopStream")

async def switch_scene(scene_name: str) -> dict:
    return await send_obs_command("SetCurrentProgramScene", {"sceneName": scene_name})