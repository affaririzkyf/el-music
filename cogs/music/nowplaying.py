import discord
from discord.ext import commands
import time

from .play import (
    current_song,
    start_time
)

from config import EMBED_COLOR

class NowPlaying(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def create_progress_bar(
        self,
        progress,
        total,
        length=12
    ):

        filled = int(
            length * progress // total
        )

        bar = (
            "━" * filled +
            "🔘" +
            "─" * (length - filled)
        )

        return bar

    @commands.command(
        aliases=["np"]
    )
    async def nowplaying(self, ctx):

        vc = ctx.voice_client

        if not vc or not vc.is_playing():

            return await ctx.send(
                "❌ Tidak ada lagu."
            )

        elapsed = int(
            time.time() - start_time
        )

        duration = 240

        progress_bar = (
            self.create_progress_bar(
                elapsed,
                duration
            )
        )

        current_min = elapsed // 60
        current_sec = elapsed % 60

        total_min = duration // 60
        total_sec = duration % 60

        embed = discord.Embed(
            title="🎵 Now Playing",
            description=(
                f"**{current_song['title']}**\n\n"
                f"`{current_min:02}:{current_sec:02}` "
                f"{progress_bar} "
                f"`{total_min:02}:{total_sec:02}`"
            ),
            color=EMBED_COLOR
        )

        embed.set_thumbnail(
            url=current_song["thumbnail"]
        )

        await ctx.send(embed=embed)