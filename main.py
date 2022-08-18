import os
import glob
import random
import logging
from time import time
import json
import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import discord
from discord.ext import tasks, commands

import topgg
#import libraries.database as db 

from dotenv import load_dotenv

# Load dotenv file
load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")#_STABLE")
TOP_GG_TOKEN = os.getenv("TOP_GG_TOKEN")
TOP_GG_PORT = os.getenv("TOP_GG_PORT")
TOP_GG_ENCRYPTION_KEY = os.getenv("TOP_GG_ENCRYPTION_KEY")

# Load config file
with open("config.json", "r") as f:
    config = json.load(f)

# Load status file
with open("statuses.json", "r") as f:
    statusjson = json.load(f)


# Grab statuses from statuses.json
statuses = statusjson["statuses"]

# Grab vars from config.json
DEFAULT_PREFIX = config["DEFAULT_PREFIX"]
SHARDS = config["SHARDS"]
OWNER_IDS = config["OWNER_IDS"]
STATUS_OUT = config["STATUS_OUT"]

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
        self.synced = True
        
        #self.scheduler = AsyncIOScheduler()
        #db.autosave(self.scheduler)
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()#guild = discord.Object(id = 628212961218920477))
            self.synced = True
        print("Slash commands are now ready!")
        

        if not bot.ready:
            
            #self.scheduler.start()

            # Start the status updater
            change_status_task.start()

            # Post new status to STATUS_OUT channel from config.json
            bot.status_out = bot.get_channel(STATUS_OUT)

            try:
                # Send a message saying how long the bot was offline for
                with open("storage/misc/time.json", "r") as f:
                    last_time = json.load(f)
                await bot.get_channel(978695335570444435).send(f"Bot back online!\n**I was offline for: {timedelta(seconds=((datetime.utcnow() - datetime(1970, 1, 1)).seconds)-int(last_time))}**")
            except:
                print("i hope this is running on alpha")


            # If the bot userid matches Andromeda's userid then connect to top.gg
            if bot.user.id == 765222621779853312:
                bot.topggobj = topgg.DBLClient(bot, TOP_GG_TOKEN, autopost=True, post_shard_count=True)

            # Create guild_count var and initialize to 0
            guild_count = 0
            # for each guild the bot is in
            for guild in bot.guilds:
                # Print guild name and id
                print(f"- {guild.id} (name: {guild.name})")
                # Increment guild_count
                guild_count = guild_count + 1

            # Print the bot name, number of guilds, and number of shards.
            print(f"{bot.user} is in {guild_count} guild(s).\nwith {bot.shard_count} shard(s)")

            # Set the bot ready to True
            bot.ready = True


# get the prefix from the server it's in
def get_prefix(bot, message):
    try:
        # Get the guild prefixes from prefixes.json file
        with open("storage/guild_data/prefixes.json", "r") as f:
            rawprefixes = json.load(f)

        # Create prefixes var
        prefixes = []
        # For each guild in prefixes.json
        for i in rawprefixes[str(message.guild.id)]:
            # Check if the prefix is not none
            if rawprefixes[str(message.guild.id)][i.lower()] != 'none':
                # Append the prefix to the prefixes var
                prefixes.append(rawprefixes[str(message.guild.id)][i])

        # Return prefixes
        return commands.when_mentioned_or(*prefixes)(bot, message)
    except:
        # If the guild is not in the prefixes.json file, return the default prefix
        return commands.when_mentioned_or(DEFAULT_PREFIX, "beav")(bot, message)


bot = MyBot(
    command_prefix = (get_prefix),
    owner_ids = OWNER_IDS,
    intents = discord.Intents.all()
)

tree = bot.tree

# @tree.command(name = "ping", description = "Pong!")
# async def ping(interaction: discord.Interaction):
#     await interaction.response.send_message(f"Pong! slash commands have a latency of {round(bot.latency * 1000)}ms")

@tree.command(name = "prefix", description = "Tells you what the bot's prefixes are")
async def ping(interaction: discord.Interaction):
    with open("storage/guild_data/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixesstr = ""
    for i in prefixes[str(interaction.guild.id)]:
        prefixesstr += f"{i}: {prefixes[str(interaction.guild.id)][i]}\n"

    await interaction.response.send_message(f"My prefixes in this server are:\n{prefixesstr}")



# Remove default help command
bot.remove_command("help")
# Set the ready status to False, so the bot knows it hasnt been initialized yet.
bot.ready = False

@bot.event
async def on_autopost_success():
    """Event for when stats are successfully updated on top.gg"""
    print(f"Posted server count ({bot.topggobj.guild_count}), shard count ({bot.shard_count})")



@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard {shard_id} Ready!")


@tasks.loop(hours=5, minutes=random.randint(0, 120))
async def change_status_task():
    # status = "changed the host, should be more stable now :)"
    # Set the status to a random status from the statuses list
    status = random.choice(statuses)
    # Check if the status is "advanced"
    if "extra-" in status:
        advanced_statuses = {
            "extra-total_users": f"{len(bot.users)} users",
            "extra-total_guilds": f"over {len(bot.guilds)} guilds",
            "extra-total_shards": f"over {bot.shard_count} shards",
        }

        # Replace the placeholder status with the advanced status.
        for key, value in advanced_statuses.items():
            status = status.replace(key, value)

    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.watching, name=(status)),
    )
    await bot.status_out.send(f'status changed to "{status}"')


# async def setup(bot):
#     print("Setting up...")
 
#     db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
# 					 ((guild.id,) for guild in bot.guilds))

#     db.commit()

async def load_cogs(bot):
    print("Loading cogs...")
    # loads cogs
    for filename in glob.iglob("./cogs/**", recursive=True):
        if filename.endswith('.py'):
            filename = filename[2:].replace("/", ".") # goes from "./cogs/economy.py" to "cogs.economy.py"
            await bot.load_extension(f'{filename[:-3]}') # removes the ".py" from the end of the filename, to make it into cogs.economy
    

async def main():
    async with bot:
        #await setup(bot)
        await load_cogs(bot)
        await bot.start(TOKEN)

asyncio.run(main())
