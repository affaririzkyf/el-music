import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True

# PREFIX ?
bot = commands.Bot(command_prefix="?", intents=intents)

# =========================
# YTDLP CONFIG
# =========================
ytdl_format_options = {
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",

    # FIX YOUTUBE BLOCK
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "web"]
        }
    },
}

ffmpeg_options = {
    "options": "-vn"
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


# =========================
# YTDL SOURCE
# =========================
class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):

        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)

        return cls(
            discord.FFmpegPCMAudio(filename, **ffmpeg_options),
            data=data
        )


# =========================
# READY EVENT
# =========================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


# =========================
# PING COMMAND
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


# =========================
# PLAY COMMAND
# =========================
@bot.command()
async def play(ctx, *, query):

    if ctx.author.voice is None:
        return await ctx.send("❌ Masuk voice channel dulu.")

    voice_channel = ctx.author.voice.channel

    # CONNECT BOT
    if ctx.voice_client is None:
        await voice_channel.connect()

    elif ctx.voice_client.channel != voice_channel:
        await ctx.voice_client.move_to(voice_channel)

    async with ctx.typing():

        try:
            player = await YTDLSource.from_url(
                query,
                loop=bot.loop,
                stream=True
            )

            ctx.voice_client.stop()

            ctx.voice_client.play(
                player,
                after=lambda e: print(f"Player Error: {e}") if e else None
            )

            await ctx.send(f"🎵 Now Playing: **{player.title}**")

        except Exception as e:
            await ctx.send(f"❌ Error:\n```{e}```")


# =========================
# STOP COMMAND
# =========================
@bot.command()
async def stop(ctx):

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Disconnected.")


# =========================
# MAIN
# =========================
async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())