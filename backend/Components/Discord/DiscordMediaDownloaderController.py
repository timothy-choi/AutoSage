import os
import aiohttp
import discord
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
SAVE_DIR = "./downloads"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = discord.Client(intents=intents)
app = FastAPI()

class DownloadRequest(BaseModel):
    channel_id: int
    limit: int = 20

download_queue = []

async def download_attachment(attachment, save_dir=SAVE_DIR):
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, attachment.filename)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status == 200:
                    with open(file_path, "wb") as f:
                        f.write(await resp.read())
                    return file_path
    except Exception as e:
        print(f"❌ Error downloading {attachment.filename}: {e}")
    return None

@app.post("/download-media")
async def trigger_media_download(req: DownloadRequest):
    download_queue.append(req)
    return {"status": "queued", "channel_id": req.channel_id, "limit": req.limit}

@bot.event
async def on_ready():
    print(f"🟢 Bot is ready as {bot.user}")

    while True:
        if download_queue:
            req = download_queue.pop(0)
            channel = bot.get_channel(req.channel_id)

            if not channel:
                print(f"❌ Channel {req.channel_id} not found.")
                continue

            print(f"📥 Downloading from channel {req.channel_id} (limit={req.limit})")
            count = 0
            async for message in channel.history(limit=req.limit):
                for attachment in message.attachments:
                    path = await download_attachment(attachment)
                    if path:
                        count += 1
            print(f"✅ Downloaded {count} file(s) from channel {req.channel_id}")

def start_discord_bot():
    import threading
    threading.Thread(target=lambda: bot.run(TOKEN)).start()

start_discord_bot()