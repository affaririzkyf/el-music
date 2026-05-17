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

# =========================
# BOT
# =========================
bot = commands.Bot(
    command_prefix="?",
    intents=intents
)

# =========================
# READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


# =========================
# PING
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


# =========================
# PLAY
# =========================
@bot.command()
async def play(ctx, *, search):

    print("PLAY COMMAND CALLED")

    await ctx.send(f"🔍 Searching: `{search}`")

    # =========================
    # CHECK VC
    # =========================
    if not ctx.author.voice:
        return await ctx.send(
            "❌ Join voice channel dulu."
        )

    channel = ctx.author.voice.channel

    # =========================
    # CONNECT VC
    # =========================
    try:

        if ctx.voice_client is None:

            await ctx.send(
                "🔌 Connecting VC..."
            )

            await asyncio.wait_for(
                channel.connect(),
                timeout=15
            )

        elif ctx.voice_client.channel != channel:

            await ctx.voice_client.move_to(
                channel
            )

        await ctx.send(
            "✅ Connected to VC"
        )

    except Exception as e:

        print(e)

        return await ctx.send(
            f"❌ VC ERROR:\n```{e}```"
        )

    # =========================
    # YTDLP CONFIG
    # =========================
    ytdl_format_options = {

        # AUDIO
        "format": "bestaudio/best",

        # QUIET
        "quiet": True,

        # SEARCH
        "default_search": "ytsearch",

        # NO PLAYLIST
        "noplaylist": True,

        # COOKIES
        "cookiefile": "cookies.txt",

        # SKIP DOWNLOAD
        "skip_download": True,

        # FIX SSL
        "nocheckcertificate": True,

        # YOUTUBE FIX
        "extractor_args": {
            "youtube": {
                "player_client": [
                    "android"
                ]
            }
        }
    }

    ytdl = yt_dlp.YoutubeDL(
        ytdl_format_options
    )

    # =========================
    # SEARCH MUSIC
    # =========================
    try:

        await ctx.send(
            "🔎 Searching YouTube..."
        )

        loop = asyncio.get_event_loop()

        # FORCE SEARCH1
        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(
                f"ytsearch1:{search}",
                download=False
            )
        )

        # SEARCH RESULT
        if "entries" in data:

            data = data["entries"][0]

        # AUDIO URL
        url = data["url"]

        # TITLE
        title = data["title"]

        await ctx.send(
            f"🎵 Found: **{title}**"
        )

        # =========================
        # PLAY AUDIO
        # =========================
        source = await discord.FFmpegOpusAudio.from_probe(
            url,
            method="fallback"
        )

        ctx.voice_client.stop()

        ctx.voice_client.play(
            source,
            after=lambda e: print(
                f"PLAYER ERROR: {e}"
            ) if e else None
        )

        await ctx.send(
            f"▶️ Now Playing:\n**{title}**"
        )

    except Exception as e:

        print(e)

        await ctx.send(
            f"❌ PLAY ERROR:\n```{e}```"
        )


# =========================
# STOP
# =========================
@bot.command()
async def stop(ctx):

    if ctx.voice_client:

        await ctx.voice_client.disconnect()

        await ctx.send(
            "👋 Disconnected"
        )


# =========================
# MAIN
# =========================
async def main():

    async with bot:

        await bot.start(TOKEN)


asyncio.run(main())