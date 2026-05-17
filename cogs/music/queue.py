import discord
from discord.ext import commands

from .play import queue
from config import EMBED_COLOR

class Queue(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def queue(self, ctx):

        if len(queue) == 0:

            return await ctx.send(
                "📭 Queue kosong."
            )

        msg = ""

        for i, song in enumerate(queue):

            msg += (
                f"{i+1}. "
                f"{song['title']}\n"
            )

        embed = discord.Embed(
            title="📜 Music Queue",
            description=msg,
            color=EMBED_COLOR
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):

        vc = ctx.voice_client

        if vc and vc.is_playing():

            vc.stop()

            await ctx.send(
                "⏭️ Lagu diskip."
            )

    @commands.command()
    async def stop(self, ctx):

        vc = ctx.voice_client

        queue.clear()

        if vc:

            await vc.disconnect()

            await ctx.send(
                "⏹️ Music dihentikan."
            )