from discord.ext import commands
from utils.player import set_filter

class Filters(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bassboost(self, ctx):

        set_filter("bassboost")

        await ctx.send(
            "🔊 Bassboost aktif."
        )

    @commands.command()
    async def nightcore(self, ctx):

        set_filter("nightcore")

        await ctx.send(
            "⚡ Nightcore aktif."
        )

    @commands.command()
    async def vaporwave(self, ctx):

        set_filter("vaporwave")

        await ctx.send(
            "🌊 Vaporwave aktif."
        )

    @commands.command()
    async def clear(self, ctx):

        set_filter("clear")

        await ctx.send(
            "✨ Clear audio aktif."
        )

    @commands.command()
    async def normal(self, ctx):

        set_filter("normal")

        await ctx.send(
            "🎵 Filter normal aktif."
        )