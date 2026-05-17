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
# PING COMMAND
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


# =========================
# PLAY COMMAND DEBUG
# =========================
@bot.command()
async def play(ctx, *, search):

    print("PLAY COMMAND CALLED")

    await ctx.send(f"🔍 Command Working: {search}")

    # CHECK VC
    if not ctx.author.voice:
        return await ctx.send("❌ Join VC dulu.")

    channel = ctx.author.voice.channel

    # CONNECT
    if ctx.voice_client is None:
        await channel.connect()

    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)

    await ctx.send("✅ Connected to VC")

    # =========================
    # YTDLP
    # =========================
    ytdl_format_options = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": False,
        "default_search": "ytsearch",
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

    try:

        loop = asyncio.get_event_loop()

        await ctx.send("🔎 Searching YouTube...")

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(search, download=False)
        )

        if "entries" in data:
            data = data["entries"][0]

        url = data["url"]
        title = data["title"]

        await ctx.send(f"🎵 Found: {title}")

        source = await discord.FFmpegOpusAudio.from_probe(
            url,
            method="fallback"
        )

        ctx.voice_client.stop()

        ctx.voice_client.play(
            source,
            after=lambda e: print(f"PLAYER ERROR: {e}") if e else None
        )

        await ctx.send(f"▶️ Playing: **{title}**")

    except Exception as e:

        print(e)

        await ctx.send(f"❌ ERROR:\n```{e}```")


# =========================
# STOP COMMAND
# =========================
@bot.command()
async def stop(ctx):

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Disconnected")


# =========================
# MAIN
# =========================
async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())