import datetime as dt
import os
import time
import logging
import discord
from discord import app_commands
from discord.ext import commands
from url import SERVER_EMOJI_LIMIT
from discord import Embed
from discord import Permissions, guild, channel, utils
from PIL import Image
from io import BytesIO
import requests
import asyncio


bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

token = "MTEzOTYwNjA3ODM4NTAzMzM3Ng.GCy4BE.kiSLGd1i2jHDseAcTr5pHqszlw73hiQGgTRI8E"


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print("Bot is ready!")
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


# creating embed with poll
@bot.tree.command(name="add-emoji", description="Add a new emoji to the server.")
@app_commands.checks.has_permissions(manage_emojis=True)
@app_commands.describe(url="What image do you want to add?", title="What should the name of this emoji be?")
async def poll(interaction: discord.Interaction, url: str, title: str):
    if at_server_limit(interaction.guild.id):
        await interaction.response.send_message("Server at emoji limit.", ephemeral=True)
        return

    if not is_new_emoji(title, interaction.guild.id):
        await interaction.response.send_message("Emoji already exists.", ephemeral=True)
        return

    await interaction.response.send_message("Creating poll...", ephemeral=True)
    await interaction.delete_original_response()

    emb = discord.Embed(color=discord.Color.blurple(), title=f"POLL TO ADD NEW EMOJI: :{title}:",
                        description="Should we add this emoji?", timestamp=dt.datetime.now())
    emb.set_image(url=f"{url}")
    emb.set_footer(text=f"Poll by {interaction.user.display_name}")

    msg = await interaction.channel.send(embed=emb)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    img = await make_image_from_url(url=url)

    def check(reaction, user):
        return user == interaction.user and reaction.emoji == "✅"
    try:
        await bot.wait_for('reaction_add', timeout=30, check=check)
        new_emoji = await interaction.channel.guild.create_custom_emoji(name=title, image=img)
        await interaction.channel.send(f"Emoji added: {str(new_emoji)}")
    except asyncio.TimeoutError:
        await interaction.channel.send("Emoji not added.")


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


async def make_image_from_url(url):
    r = requests.get(url)
    poll_img = Image.open(BytesIO(r.content), mode='r')
    img = poll_img.resize((128, 128))
    b = BytesIO()
    img.save(b, "PNG")
    b_value = b.getvalue()

    return b_value


bot.run(token)





