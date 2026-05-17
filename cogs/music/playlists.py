import discord
from discord.ext import commands
import json
import os

from .play import queue
from config import EMBED_COLOR

class Playlists(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.playlist_file = (
            "data/playlists.json"
        )

    def load_playlists(self):

        if not os.path.exists(
            self.playlist_file
        ):

            return {}

        with open(
            self.playlist_file,
            "r"
        ) as f:

            return json.load(f)

    def save_playlists(self, data):

        with open(
            self.playlist_file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    @commands.command()
    async def save(self, ctx, name):

        if len(queue) == 0:

            return await ctx.send(
                "📭 Queue kosong."
            )

        data = self.load_playlists()

        data[name] = queue

        self.save_playlists(data)

        await ctx.send(
            f"❤️ Playlist `{name}` disimpan."
        )

    @commands.command()
    async def load(self, ctx, name):

        data = self.load_playlists()

        if name not in data:

            return await ctx.send(
                "❌ Playlist tidak ditemukan."
            )

        queue.extend(data[name])

        await ctx.send(
            f"📂 Playlist `{name}` dimuat."
        )

    @commands.command()
    async def playlists(self, ctx):

        data = self.load_playlists()

        if len(data) == 0:

            return await ctx.send(
                "📭 Belum ada playlist."
            )

        msg = ""

        for name in data:

            msg += f"• {name}\n"

        embed = discord.Embed(
            title="❤️ Saved Playlists",
            description=msg,
            color=EMBED_COLOR
        )

        await ctx.send(embed=embed)