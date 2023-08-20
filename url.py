import discord
import requests
from PIL import Image
from io import BytesIO


SERVER_EMOJI_LIMIT = 50
WAIT_TIMES_BETWEEN_CHECKS = 15
POLL_YES_EMOJI = "✅"
POLL_NO_EMOJI = "❌"


async def make_image_from_url(url):
    r = requests.get(url)
    poll_img = Image.open(BytesIO(r.content), mode='r')
    img = poll_img.resize((128, 128))
    b = BytesIO()
    img.save(b, "PNG")
    b_value = b.getvalue()

    return b_value


async def get_votes(message: discord.Message, self_bot_id: int):
    yes_count = []
    no_count = []
    for reaction in message.reactions:
        if reaction.emoji == POLL_YES_EMOJI:
            async for user in reaction.users():
                if user.id == self_bot_id:
                    continue
                else:
                    yes_count.append(user)
        elif reaction.emoji == POLL_NO_EMOJI:
            async for user in reaction.users():
                if user.id == self_bot_id:
                    continue
                else:
                    no_count.append(user)

    return yes_count, no_count


async def get_poll_result(message: discord.Message, self_bot_id: int, yes_count=None, no_count=None):
    if yes_count is None and no_count is None:
        yes_count, no_count = await get_votes(message, self_bot_id)
    if len(yes_count) + len(no_count) == 0:
        return False
    else:
        if len(yes_count) > len(no_count):
            return True
        else:
            return False


def get_emoji_name_from_poll_message(message: discord.Message, new=False):
    if new:
        return message.embeds[0].title.split(":")[4]
    else:
        return message.embeds[0].title.split(":")[2]
