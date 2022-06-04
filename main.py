import os
import glob
import random
import logging
from time import time
import json

from datetime import datetime, timedelta
import topgg

import discord
from discord.ext import tasks, commands

from dotenv import load_dotenv

load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")#_STABLE")
TOP_GG_TOKEN = os.getenv("TOP_GG_TOKEN")
TOP_GG_PORT = os.getenv("TOP_GG_PORT")
TOP_GG_ENCRYPTION_KEY = os.getenv("TOP_GG_ENCRYPTION_KEY")

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
async def on_autopost_success():
    print(f"Posted server count ({bot.topggobj.guild_count}), shard count ({bot.shard_count})")


@bot.event
async def on_dbl_vote(data):
    """An event that is called whenever someone votes for the bot on Top.gg."""
    if data["type"] == "test":
        # this is roughly equivalent to
        # `return await on_dbl_test(data)` in this case
        #return bot.dispatch("dbl_test", data)
        on_dbl_test(data)

    print(f"Received a vote:\n{data}")


@bot.event
async def on_dbl_test(data):
    """An event that is called whenever someone tests the webhook system for your bot on Top.gg."""
    print(f"Received a test vote:\n{data}")


@bot.event
async def on_ready():
    if not bot.ready:


        change_status_task.start()

        bot.status_out = bot.get_channel(STATUS_OUT)
        
        try:
            with open("storage/misc/time.json", "r") as f:
                last_time = json.load(f)
            #await bot.get_channel(978695335570444435).send(f"Bot back online!\n**I was offline for: {timedelta(seconds=((datetime.utcnow() - datetime(1970, 1, 1)).seconds)-int(last_time))}**")
        except:
            print("i hope this is running on alpha")
        

        if bot.user.id == 765222621779853312:
            bot.topggobj = topgg.DBLClient(bot, TOP_GG_TOKEN, autopost=True, post_shard_count=True)
               
            
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
