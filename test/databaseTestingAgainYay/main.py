import aiosqlite

# yeah no this is painful i'm sticking with a json file even though i REALLY shuoldn't lmao

import os
import glob
import logging
from time import time
import asyncio

import discord
from discord.ext import tasks, commands

from dotenv import load_dotenv

# Load dotenv file
load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")  # _STABLE")

# Logging
logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{time()}.log",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

logging.warning("warning")
logging.error("error")
logging.critical("critical")


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        await self.wait_until_ready()

        print(f"Logged in as {self.user}")

        if not bot.ready:
            async with aiosqlite.connect("main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(
                        "CREATE TABLE IF NOT EXISTS users (id INTEGER, guild INTEGER)"
                    )

                await db.commit()

                print(db)

            bot.ready = True


bot = MyBot(command_prefix="q", intents=discord.Intents.all())

tree = bot.tree


@bot.command()
async def adduser(ctx, member: discord.Member):
    member = ctx.author
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                "SELECT id FROM users WHERE guild = ?", (ctx.guild.id,)
            )
            data = await cursor.fetchone()
            if data:
                await cursor.execute(
                    "UPDATE users SET id = ? WHERE guild = ?",
                    (
                        member.id,
                        ctx.guild.id,
                    ),
                )
            else:
                await cursor.execute(
                    "INSERT INTO users (id, guild) VALUES (?, ?)",
                    (
                        member.id,
                        ctx.guild.id,
                    ),
                )
        await db.commit()


@bot.command()
async def removeuser(ctx, member: discord.Member):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                "SELECT id FROM users WHERE guild = ?", (ctx.guild.id,)
            )
            data = await cursor.fetchone()
            if data:
                await cursor.execute(
                    "DELETE FROM users WHERE id = ? AND guild = ?",
                    (
                        member.id,
                        ctx.guild.id,
                    ),
                )
        await db.commit()


# Remove default help command
bot.remove_command("help")
# Set the ready status to False, so the bot knows it hasnt been initialized yet.
bot.ready = False


async def load_cogs(bot):
    print("Loading cogs...")
    # loads cogs
    for filename in glob.iglob("./cogs/**", recursive=True):
        if filename.endswith(".py"):
            filename = filename[2:].replace(
                "/", "."
            )  # goes from "./cogs/economy.py" to "cogs.economy.py"
            await bot.load_extension(
                f"{filename[:-3]}"
            )  # removes the ".py" from the end of the filename, to make it into cogs.economy


async def main():
    async with bot:
        # await setup(bot)
        # await load_cogs(bot)
        await bot.start(TOKEN)


asyncio.run(main())
