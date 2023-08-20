import datetime as dt
import os
import time
import discord
from discord import app_commands
from discord.ext import commands
from url import SERVER_EMOJI_LIMIT
from url import POLL_YES_EMOJI
from url import POLL_NO_EMOJI
from discord import Embed
from discord import Permissions, guild, channel, utils
import asyncio


token = "Your bot token here"

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())

if "active_polls" not in os.listdir():
    os.mkdir("active_polls")


# creating embed with poll
@bot.tree.command(name="add-emoji", description="Creates a poll for a new emoji.")
@app_commands.describe(url="URL of new emoji source picture", title="What we should call this new emoji.")
async def create_poll(interaction: discord.Interaction, url: str, title: str):
    if at_server_limit(interaction.guild_id):
        await interaction.response.send_message("Server has reached emoji limit.", ephemeral=True)
        return

    if not is_new_emoji(name=title, guild_id=interaction.guild_id):
        await interaction.response.send_message("Emoji already exists.", ephemeral=True)
        return

    embed = discord.Embed(colour=discord.Color.blurple(), title=f"POLL FOR NEW EMOJI: :{title}:",
                          description="Should we add this emoji?", timestamp=dt.datetime.now())
    embed.set_image(url=url)
    await interaction.response.send_message("Creating poll...", ephemeral=True)
    await interaction.delete_original_response()
    msg = await interaction.channel.send(embed=embed)
    await msg.add_reaction(POLL_YES_EMOJI)
    await msg.add_reaction(POLL_NO_EMOJI)

    save_poll_to_memory(interaction.guild_id, interaction.channel_id, msg.id)


def at_server_limit(guild_id: int):
    guild_name = bot.get_guild(guild_id)
    existing_emojis = []
    for emoji in guild_name.emojis:
        if emoji is not None:
            existing_emojis.append(emoji)
    if existing_emojis is not None:
        if len(existing_emojis) == SERVER_EMOJI_LIMIT:
            return True
        else:
            return False


def is_new_emoji(name: str, guild_id: int):
    guild_name = bot.get_guild(guild_id)
    existing_emoji_names = []
    for emoji in guild_name.emojis:
        if emoji is not None:
            existing_emoji_names.append(emoji.name)
    if name not in existing_emoji_names:
        return True
    else:
        return False


def save_poll_to_memory(guild_id, channel_id, message_id):
    try:
        os.mkdir(f"active_polls/{guild_id}")
    except FileExistsError:
        pass
    finally:
        try:
            os.mkdir(f"active_polls/{guild_id}/{channel_id}")
        except FileExistsError:
            pass
    f = open(
        f"active_polls/{guild_id}/{channel_id}/{message_id}",
        "w",
    )
    f.close()


bot.run(token)





