import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import PREFIX
import os
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():

    print(f"Login sebagai {bot.user}")

    try:

        synced = await bot.tree.sync()

        print(
            f"Synced {len(synced)} slash commands"
        )

    except Exception as e:
        print(e)
    

async def load_cogs():

    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.events")

async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)

asyncio.run(main())