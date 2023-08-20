import asyncio
import os
from url import make_image_from_url
from url import get_votes
from url import get_poll_result
from url import get_emoji_name_from_poll_message
from url import WAIT_TIMES_BETWEEN_CHECKS
import datetime as dt
import discord
import logging

token = "Your bot token here"

if "active_polls" not in os.listdir():
    os.mkdir("active_polls")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)


def get_active_polls_from_memory():
    combos = []
    for guild_id in os.listdir("active_polls"):
        for channel_id in os.listdir(f"active_polls/{guild_id}"):
            for message_id in os.listdir(f"active_polls/{guild_id}/{channel_id}"):
                combos.append((int(guild_id), int(channel_id), int(message_id)))
    return combos


@client.event
async def on_ready():
    while True:
        for (guild_id, channel_id, message_id) in get_active_polls_from_memory():
            try:
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                if (dt.datetime.now(dt.timezone.utc) - message.created_at).seconds > 60:
                    yes_count, no_count = await get_votes(message, self_bot_id=client.user.id)
                    if await get_poll_result(message, self_bot_id=client.user.id, yes_count=yes_count, no_count=no_count):
                        name = get_emoji_name_from_poll_message(message)
                        img = await make_image_from_url(url=message.embeds[0].image.url)
                        new_emoji = await message.guild.create_custom_emoji(name=name, image=img)
                        await channel.send(f"Emoji added: {str(new_emoji)}")
                    os.remove(f"active_polls/{guild_id}/{channel.id}/{message.id}")
            except discord.errors.NotFound:
                logging.info(
                    f"Message {guild_id}-{channel_id}-{message_id} not found, skipping"
                            )
                try:
                    os.remove(
                        f"active_polls/{guild_id}/{channel_id}/{message_id}"
                            )
                except FileNotFoundError:
                    pass
        await asyncio.sleep(WAIT_TIMES_BETWEEN_CHECKS)


client.run(token)






