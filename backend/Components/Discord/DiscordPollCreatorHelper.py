import discord

EMOJI_NUMBERS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

async def create_poll(bot, channel_id: int, question: str, options: list[str]) -> str:
    if not (2 <= len(options) <= 10):
        return "Poll must have between 2 and 10 options."

    channel = bot.get_channel(channel_id)
    if not channel:
        return f"Channel {channel_id} not found."

    description = "\n".join(f"{EMOJI_NUMBERS[i]} {opt}" for i, opt in enumerate(options))
    embed = discord.Embed(title=f"\U0001F4CA {question}", description=description)

    message = await channel.send(embed=embed)
    for i in range(len(options)):
        await message.add_reaction(EMOJI_NUMBERS[i])

    return f"Poll sent to channel {channel_id}."

async def close_poll(bot, channel_id: int, message_id: int, note: str = "\U0001F6D1 Poll Closed") -> str:
    channel = bot.get_channel(channel_id)
    if not channel:
        return "Channel not found."

    try:
        message = await channel.fetch_message(message_id)
        if message.embeds:
            embed = message.embeds[0]
            embed.set_footer(text=note)
            await message.edit(embed=embed)
            return f"Poll {message_id} closed."
        else:
            return "Message has no embed."
    except Exception as e:
        return f"Error closing poll: {e}"

async def get_poll_results(bot, channel_id: int, message_id: int) -> dict:
    channel = bot.get_channel(channel_id)
    if not channel:
        return {"error": "Channel not found."}

    try:
        message = await channel.fetch_message(message_id)
        results = {}
        for reaction in message.reactions:
            if reaction.emoji in EMOJI_NUMBERS:
                count = reaction.count - 1
                results[reaction.emoji] = count
        return results
    except Exception as e:
        return {"error": str(e)}

async def delete_poll(bot, channel_id: int, message_id: int) -> str:
    channel = bot.get_channel(channel_id)
    if not channel:
        return "Channel not found."

    try:
        message = await channel.fetch_message(message_id)
        await message.delete()
        return f"Poll {message_id} deleted."
    except Exception as e:
        return f"Error: {e}"