import os
import random
import logging
from time import time

import discord  
from discord.ext import tasks, commands


from dotenv import load_dotenv

load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")

statuses = [
    "you",
    "the sky",
    "vtubers play The Sims 4",
    "goggy play meincraf",
    "my friends, their souls to be exact",
    ' fire, thinking "ooo, shiny"',
    "the sun...",
    "into s p a a c e",
    "a doublee rainbowww",
    "teknobled",
    "youtube ruin it's TOS for the 284th time",
    "rick and morty? idk i'm not a weeb",
    "bees",
    "upon the galaxy",
    "star wars - a new mistake",
    "the clock",
    "daily dose of internet",
    "my friend step on a corn flake",
    "my cereal killer friend",
    "stalin standing on a straight circle",
    "the cashier whilst they're confused at the fact i want a green pen with red ink",
    "random cat videos",
    "you realize cats can jump over six times their lenght",
    "a cat with 18 toes",
    "strangers implode after learning them how to play 5D chess",
    "my terraria farm actually work",
    "my summons killing thousands of enemies, still without dropping a rod of discord",
    "mark succy burg",
    "amogus mem es",
    "https://youtu.be/VY-PqPpyRVU",
    "good luck techno <3",
    "myself in the mirror whilst i'm doing yo mom",
    "shrek 5",
    "idk? netflix?? i'm not a normiee idk",
    "yo mom",
    "amazon break another 7924 laws",
    "you <3",
    "beavers :D",
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "... watching ... watching ... watc",
    "frogs :)",
    "beav",
    "PLEASE DON'T SING LAST CHRISTMAS RIGHT NOW APELSDFOIANFIW",
    "yet another 2981 hours of youtube",
    "<3",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "beav clicker",
    "you playin video game (you're really bad btw)",
    "wait can i put emojis in here? 🦫💓",
    "🦫🐝 (i'm not sorry)",
    "hehehe beav",
    "shrek 91847109832470192743197234718797239489.5",
    "da bee movi",
    "timberborn my beloved <3",
    "my beloved, you <3",
    "what do i even put here?",
    "amogus",
    "you bein sus uwu",
    "cookie clicker < coochie clicker",
    "holy fuck beaver make me go :)))",
    "the co- i mean clock",
    "henwee ;)",
    "bevers",
    "bævere",
    "beavers",
    "beaver dams",
    "dams",
    "Bībā",
    "beavers :)",
    "do your dailies!",
]


OWNER_IDS = [368423564229083137]
GUILD = 694107776015663146
STANDARD_OUT = 805175024762748929
WELCOME_OUT = 694197942000680980
LOGS_OUT = 844979417449234442


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
    return commands.when_mentioned_or("a!")(bot, message)


bot = commands.Bot(command_prefix=(get_prefix), owner_ids=OWNER_IDS, intents=discord.Intents.all())

bot.remove_command("help")
bot.ready = False


@bot.event
async def on_ready():
    if not bot.ready:

        change_status_task.start()

        bot.guild = bot.get_guild(GUILD)
        bot.standard_out = bot.get_channel(STANDARD_OUT)
        bot.log_out = bot.get_channel(LOGS_OUT)
        bot.welcome_out = bot.get_channel(WELCOME_OUT)
        bot.status_out = bot.get_channel(848925880360632350)

        guild_count = 0
        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count = guild_count + 1

        print(f"{bot.user} is in " + str(guild_count) + " guild(s).")

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
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run((TOKEN), bot=True, reconnect=True)
