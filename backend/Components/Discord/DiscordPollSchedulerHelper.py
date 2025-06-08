import asyncio
from datetime import datetime
from typing import List, Dict
import discord

scheduled_polls: List[Dict] = []

def schedule_poll(channel_id: int, question: str, options: List[str], send_at: datetime):
    if len(options) < 2 or len(options) > 10:
        raise ValueError("Poll must have 2–10 options.")
    scheduled_polls.append({
        "channel_id": channel_id,
        "question": question,
        "options": options,
        "send_at": send_at,
        "sent": False
    })

EMOJI_NUMBERS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

async def poll_scheduler_loop(bot):
    while True:
        now = datetime.utcnow()
        for poll in scheduled_polls:
            if not poll["sent"] and now >= poll["send_at"]:
                channel = bot.get_channel(poll["channel_id"])
                if channel:
                    description = "\n".join(f"{EMOJI_NUMBERS[i]} {opt}" for i, opt in enumerate(poll["options"]))
                    embed = discord.Embed(title=f"📊 {poll['question']}", description=description)
                    message = await channel.send(embed=embed)

                    for i in range(len(poll["options"])):
                        await message.add_reaction(EMOJI_NUMBERS[i])
                    poll["sent"] = True
        await asyncio.sleep(5)