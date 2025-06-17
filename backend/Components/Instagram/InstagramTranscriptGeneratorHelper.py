import aiohttp
import json

async def get_video_url(media_id: str, access_token: str) -> str:
    url = f"https://graph.facebook.com/v19.0/{media_id}?fields=media_type,media_url&access_token={access_token}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            if data.get("media_type") == "VIDEO":
                return data.get("media_url")
            return None

async def generate_transcript_from_video(media_url: str, whisper_api_key: str) -> dict:
    whisper_url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {whisper_api_key}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(whisper_url, headers=headers, data={"file": media_url, "model": "whisper-1"}) as resp:
            if resp.status != 200:
                return {"error": f"Transcription failed: HTTP {resp.status}", "details": await resp.text()}
            return await resp.json()