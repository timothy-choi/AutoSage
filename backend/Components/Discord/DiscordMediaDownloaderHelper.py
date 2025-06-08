import discord
import aiohttp
import os

TOKEN = "YOUR_BOT_TOKEN_HERE"
SAVE_DIR = "./downloads"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🟢 Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.attachments:
        os.makedirs(SAVE_DIR, exist_ok=True)
        for attachment in message.attachments:
            file_path = os.path.join(SAVE_DIR, attachment.filename)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            with open(file_path, "wb") as f:
                                f.write(await resp.read())
                            print(f"✅ Downloaded: {attachment.filename}")
            except Exception as e:
                print(f"❌ Failed to download {attachment.filename}: {e}")

client.run(TOKEN)