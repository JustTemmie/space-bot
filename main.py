import os
import glob
import random
import logging
from time import time
import json

import discord  
from discord.ext import tasks, commands


from dotenv import load_dotenv

load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")

with open("config.json", "r") as f:
    config = json.load(f)

with open("statuses.json", "r") as f:
    statusjson = json.load(f)


statuses = statusjson["statuses"]

DEFAULT_PREFIX = config["DEFAULT_PREFIX"]
SHARDS = config["SHARDS"]
OWNER_IDS = config["OWNER_IDS"]
STATUS_OUT = config["STATUS_OUT"]


logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{time()}.log",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)


logging.warning("warning")
logging.error("error")
logging.critical("critical")


def get_prefix(bot, message):
    # try:
    # prefix = db[f"prefix_{message.guild.id}"]
    # return commands.when_mentioned_or(prefix)(bot, message)
    # except:
    return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)


bot = commands.AutoShardedBot(
    shard_count=SHARDS,
    command_prefix=(get_prefix),
    owner_ids=OWNER_IDS,
    intents=discord.Intents.all()
)

bot.remove_command("help")
bot.ready = False


@bot.event
async def on_ready():
    if not bot.ready:
        
        change_status_task.start()

        bot.status_out = bot.get_channel(848925880360632350)

        guild_count = 0
        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count = guild_count + 1

        print(f"{bot.user} is in {guild_count} guild(s).\nwith {bot.shard_count} shard(s)")

        bot.ready = True


async def randomize_status():
    # status = "changed the host, should be more stable now :)"
    status = random.choice(statuses)
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.watching, name=(status)),
    )
    await bot.status_out.send(f'status changed to "{status}"')


@tasks.loop(hours=5, minutes=random.randint(0, 120))
async def change_status_task():
    await randomize_status()


# loads cogs
for filename in glob.iglob("./cogs/**", recursive=True):
    if filename.endswith('.py'):
        filename = filename[2:].replace("/", ".") # goes from "./cogs/economy.py" to "cogs.economy.py"
        bot.load_extension(f'{filename[:-3]}') # removes the ".py" from the end of the filename, to make it into cogs.economy

bot.run((TOKEN), bot=True, reconnect=True)
