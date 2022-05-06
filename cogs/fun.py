import discord
from discord import Member, File, Embed, Intents, Object, NotFound
from discord.errors import HTTPException, Forbidden
from discord.utils import find
from discord.ext import tasks, commands

# from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import (
    cooldown,
    BucketType,
    CommandNotFound,
    BadArgument,
    MissingRequiredArgument,
    CommandOnCooldown,
    when_mentioned_or,
    command,
    has_permissions,
    bot_has_permissions,
    Greedy,
    Converter,
    CheckFailure,
    Cog,
    MissingRequiredArgument,
)

from datetime import datetime, timedelta
from aiohttp import request
import requests
import urllib
import re
from asyncio import sleep
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json

import random
import os

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
tenor_api_key = os.getenv("TENOR")
deepai_key = os.getenv("DEEP_AI")


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="texttoimage",
        aliases=["tti", "imageapi"],
        brief="takes a string of text and converts it to an image, don't ask",
    )
    @cooldown(5, 10, BucketType.user)
    async def texttoimageapi(self, ctx, *, content):
        r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                "text": (content),
            },
            headers={"api-key": deepai_key},
        )

        output = r.json()
        realoutput = output["output_url"]

        embed = discord.Embed(
            title=f"{ctx.author.display_name} just API'd {content}",
            colour=ctx.author.colour,
        )
        if realoutput is not None:
            embed.set_image(url=realoutput)

        await ctx.send(embed=embed)

    @commands.command(
        name="pot",
        aliases=["potter", "otterpog"],
        brief="a referance to the best meme ever made",
    )
    @cooldown(5, 10, BucketType.guild)
    async def pot_command(self, ctx):
        await ctx.send("POTTERRRRR!!!!!!!")
        await ctx.send(file=File("./images/potter.png"))

    @commands.command(name="rick", aliases=["rickroll"], brief="never gonna give you up")
    @cooldown(5, 10, BucketType.guild)
    async def dancin_man_rick(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    @commands.command(
        name="tenor",
        aliases=["gif"],
        brief="sends a gif from tenor using the given term",
    )
    @cooldown(2, 5, BucketType.guild)
    async def tenor_search(self, ctx, value=str(0), *, search_term=None):
        if search_term is None or value == str(0):
            await ctx.send(
                f"please specify what you want to search up, and how many of the top results you want to look thru\n\nfor exmaple: {ctx.prefix}tenor 6 dog\nwill pick one of the top `6` results for `dog` and send it"
            )
            return

        if search_term is not None:
            r = requests.get(
                "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s"
                % (search_term, tenor_api_key, int(value))
            )

            if r.status_code == 200:
                top_x_gifs = json.loads(r.content)
                # random_gif = random.choice(top_x_gifs)
                realoutput = top_x_gifs["results"][random.randrange(0, (int(value)))]["itemurl"]
                await ctx.send(realoutput)
            else:
                await ctx.send(f"i couldn't seem to find anything related to `{search_term}`")

    @commands.command(
        name="shitpost", aliases=["funnyhaha"], brief="sends a funny haha commit moment"
    )
    @cooldown(5, 20, BucketType.guild)
    async def shitpost_video(self, ctx, *, funny=None):
        with open("data/shitpost.json", "r") as f:
            shitposts = json.load(f)

        await ctx.send(random.choice(shitposts["list"]))

    @commands.command(
        name="avatar",
        aliases=["pfp"],
        brief="sends the profile picture of a specified user",
    )
    @cooldown(5, 10, BucketType.guild)
    async def avatar(self, ctx, user: discord.Member = None, dm_or_not=None):
        if user is None:
            user = ctx.author

        if dm_or_not == "dm" or dm_or_not == "DM":
            await user.send(f"{user.avatar_url}")

        else:
            await ctx.send(f"{user.avatar_url}")

    @commands.command(
        name="mock",
        aliases=["taunt", "tease", "scoff", "makefunof"],
        brief="bully a user, anyone, not me though, please - also jovi, fuck you <3 (platonically)",
    )
    @cooldown(50, 600, BucketType.user)
    async def mocksomeoneidk(self, ctx, mockee=None, *, makefunof_input=None):
        if mockee == None or makefunof_input == None:
            await ctx.send(
                f"give me an input, fool - for example **{ctx.prefix}mock <person you want to mock, either use a single word - or tag someone> <what the idiot said>**"
            )
            return

        makefunof_output = ""
        for i in range(len(makefunof_input)):
            if i % 2 == 0:
                makefunof_output += makefunof_input[i]
            else:
                makefunof_output += makefunof_input[i].upper()
        await ctx.send(f"**{mockee}:**\n{makefunof_output}")

    @commands.command(
        name="alientohuman",
        aliases=["ath"],
        brief="translates alien characters into latin ones",
    )
    @cooldown(10, 45, BucketType.user)
    async def translatealien(self, ctx, *, input=None):
        if input == None:
            await ctx.send("give me an input, fool")
            return
        human = "abcdefghijklmnopqrstuvwxyz"
        alien = "⏃⏚☊⎅⟒⎎☌⊑⟟⟊☍⌰⋔⋏⍜⌿⍾⍀⌇⏁⎍⎐⍙⌖⊬⋉"
        alien_to_human = {alien[i]: human[i] for i in range(len(alien))}
        output = ""
        for ch in input:
            output += alien_to_human.get(ch.lower(), ch)

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s translation", colour=ctx.author.colour
        )
        embed.add_field(name="input", value=f"{input}", inline=False)
        embed.add_field(name="output", value=f"{output}")
        await ctx.send(embed=embed)

    @commands.command(
        name="humantoalien",
        aliases=["hta"],
        brief="translates the latin alphabet into alien",
    )
    @cooldown(10, 45, BucketType.user)
    async def translatehuman(self, ctx, *, input=None):
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=1):
            messages.append(message)

        if input == None:
            input = f"{messages}"

        human = "abcdefghijklmnopqrstuvwxyz"
        alien = "⏃⏚☊⎅⟒⎎☌⊑⟟⟊☍⌰⋔⋏⍜⌿⍾⍀⌇⏁⎍⎐⍙⌖⊬⋉"
        human_to_alien = {human[i]: alien[i] for i in range(len(human))}
        output = ""
        for ch in input:
            output += human_to_alien.get(ch.lower(), ch)

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s translation", colour=ctx.author.colour
        )
        embed.add_field(name="input", value=f"{input}", inline=False)
        embed.add_field(name="output", value=f"{output}")
        await ctx.send(embed=embed)

    @commands.command(
        name="morse",
        aliases=["htm", "humantomorse"],
        brief="translates the latin alphabet into morse code",
    )
    @cooldown(10, 45, BucketType.user)
    async def human_to_morse(self, ctx, *, input: str):
        output = ""

        for i in input:
            if i in to_morse:
                output += to_morse[i]
            else:
                output += "<?>"
            output += "  "

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s translation", colour=ctx.author.colour
        )
        embed.add_field(name="input", value=f"{input}", inline=False)
        embed.add_field(name="output", value=f"{output}")
        await ctx.send(embed=embed)

    @commands.command(name="ping", aliases=["pong", "latency"], brief="P O N G")
    @cooldown(3, 5, BucketType.guild)
    async def ping_pong(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(
        name="fact",
        aliases=["info", "animal"],
        brief="Tells you a random fact about the specified animal",
        description="The list of animals you can ask facts about are, dog, cat, panda, fox, bird, koala",
    )
    @cooldown(3, 5, BucketType.guild)
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in (
            "dog",
            "cat",
            "panda",
            "fox",
            "bird",
            "koala",
        ):
            fact_url = f"https://some-random-api.ml/facts/{ animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(
                        title=f"A random fact about {animal.title()}s",
                        description=data["fact"],
                        colour=ctx.author.colour,
                    )
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    embed.add_field(
                        name="note",
                        value="these are taken from the internet, take them with a grain of salt",
                    )
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send(
                "No facts are available for that animal, The list of animals you can ask facts about are dog, cat, panda, fox, bird, koala."
            )

    @commands.command(name="joke", aliases=["funny"], brief="they're all horrible. Seriously")
    @cooldown(3, 5, BucketType.guild)
    async def tell_joke(self, ctx):
        await ctx.channel.trigger_typing()
        req = requests.get("https://icanhazdadjoke.com", headers={"Accept": "text/plain"})
        content = req.content.decode("UTF-8")

        await ctx.send(content)

    @commands.command(name="funfact", aliases=["ff"], brief="Fun fact. U gei")
    @cooldown(2, 4, BucketType.guild)
    async def fact_command(self, ctx):
        await ctx.channel.trigger_typing()
        text = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()["text"]
        await ctx.send(text)

    @commands.command(name="bill", aliases=["belikebill"], brief="be like bill")
    @cooldown(4, 10, BucketType.guild)
    async def be_like_bill(self, ctx, *, name="Bill"):
        link = "https://belikebill.ga/billgen-API.php?default=1&name=" + urllib.parse.quote(name)
        await ctx.send(embed=discord.Embed().set_image(url=link))

    @commands.command(
        name="dice",
        aliases=["roll"],
        brief="Roll some virtual dice! dice <amount of dice>d<wanted sides on dice>",
    )
    @cooldown(1, 3, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(value) for value in die_string.split("d"))

        if dice <= 25:
            rolls = [random.randrange(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

        else:
            await ctx.send("I can't roll that many dice. Please roll less than 25 of them")

    @roll_dice.error
    async def roll_dice_error(self, ctx, exc):
        if isinstance(exc.original, HTTPException):
            await ctx.send("The result was too large. Please try a lower number.")

        elif isinstance(exc.original, MissingRequiredArgument):
            await ctx.send("what")

    # instead of using this we rather limited the number of dice as HTTPException is wack


def setup(bot):
    bot.add_cog(fun(bot))


# '''
# LOOKUP TABLES
# '''


to_morse = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    " ": " / ",
}
