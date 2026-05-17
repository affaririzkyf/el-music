import discord

from config import (
    EMBED_COLOR,
    BOT_NAME
)

def music_embed(
    title,
    description,
    thumbnail=None
):

    embed = discord.Embed(

        title=title,

        description=description,

        color=EMBED_COLOR
    )

    embed.set_footer(
        text=BOT_NAME
    )

    if thumbnail:

        embed.set_thumbnail(
            url=thumbnail
        )

    return embed