from discord.ext import commands
from discord import app_commands
import discord

import asyncio
import time

from views.music_controls import MusicControls

from utils.player import create_source

from utils.spotify import (
    is_spotify_url,
    get_spotify_track
)

from utils.youtube import (
    search_youtube
)

from config import EMBED_COLOR

queue = []

current_song = {}

start_time = 0

class Play(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    # =========================
    # PLAY NEXT
    # =========================

    async def play_next(self, ctx):

        global current_song
        global start_time

        if len(queue) > 0:

            song = queue.pop(0)

            current_song = song

            start_time = time.time()

            source = create_source(
                song["url"]
            )

            vc = ctx.voice_client

            vc.play(
                source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(ctx),
                    self.bot.loop
                )
            )

            embed = discord.Embed(
                title="🎵 El Music",
                description=(
                    f"▶️ Sekarang memutar:\n"
                    f"**{song['title']}**"
                ),
                color=EMBED_COLOR
            )

            embed.set_thumbnail(
                url=song["thumbnail"]
            )

            await ctx.send(
                embed=embed,
                view=MusicControls()
            )

    # =========================
    # PREFIX PLAY
    # =========================

    @commands.command()
    async def play(
        self,
        ctx,
        *,
        search
    ):

        if not ctx.author.voice:

            return await ctx.send(
                "❌ Masuk voice channel dulu."
            )

        voice_channel = (
            ctx.author.voice.channel
        )

        if ctx.voice_client is None:

            await voice_channel.connect()

        # =========================
        # SPOTIFY DETECT
        # =========================

        if is_spotify_url(search):

            await ctx.send(
                "🎧 Spotify link terdeteksi."
            )

            search = get_spotify_track(
                search
            )

            if not search:

                return await ctx.send(
                    "❌ Spotify track gagal dibaca."
                )

            await ctx.send(
                f"🔎 Mencari: `{search}`"
            )

        else:

            await ctx.send(
                f"🔎 Mencari `{search}`..."
            )

        try:

            song = search_youtube(
                search
            )

            queue.append(song)

            await ctx.send(
                f"✅ Ditambahkan:\n"
                f"**{song['title']}**"
            )

            vc = ctx.voice_client

            if not vc.is_playing():

                await self.play_next(ctx)

        except Exception as e:

            print(e)

            await ctx.send(
                f"❌ Error:\n```{e}```"
            )

    # =========================
    # SLASH PLAY
    # =========================

    @app_commands.command(
        name="play",
        description="Putar lagu"
    )
    async def slash_play(
        self,
        interaction,
        search: str
    ):

        if not interaction.user.voice:

            return await (
                interaction.response.send_message(
                    "❌ Masuk voice dulu.",
                    ephemeral=True
                )
            )

        voice_channel = (
            interaction.user
            .voice.channel
        )

        if (
            interaction.guild
            .voice_client is None
        ):

            await voice_channel.connect()

        # =========================
        # SPOTIFY DETECT
        # =========================

        if is_spotify_url(search):

            await (
                interaction.response.send_message(
                    "🎧 Spotify link terdeteksi."
                )
            )

            search = get_spotify_track(
                search
            )

            if not search:

                return await (
                    interaction.followup.send(
                        "❌ Spotify gagal dibaca."
                    )
                )

            await (
                interaction.followup.send(
                    f"🔎 Mencari `{search}`"
                )
            )

        else:

            await (
                interaction.response.send_message(
                    f"🔎 Mencari `{search}`..."
                )
            )

        try:

            song = search_youtube(
                search
            )

            queue.append(song)

            vc = (
                interaction.guild
                .voice_client
            )

            if not vc.is_playing():

                fake_ctx = (
                    await self.bot.get_context(
                        await interaction.original_response()
                    )
                )

                await self.play_next(
                    fake_ctx
                )

        except Exception as e:

            print(e)

            await (
                interaction.followup.send(
                    f"❌ Error:\n```{e}```"
                )
            )