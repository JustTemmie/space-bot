import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import (
    cooldown,
    BucketType,
    Greedy,
)

import asyncio
import json
from aiohttp import request
import random
import requests

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
tenor_api_key = os.getenv("TENOR")

import libraries.standardLib as SL
from libraries.economyLib import confirmations

class social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name="rape", aliases=["sex", "r4pe", "r4p3", "rap3", "epar", "pare", "reap", "raape", "raaape", "raaaape", "rapee"], hidden = True)
    # async def rapeisbad(self, ctx, member:discord.Member):
    #    member = ctx.author
    #    await ctx.send(f"{ctx.author} tried to rape someone, to stop this from happening in the future they have been kicked from the server")
    #    await member.kick(reason="tried to rape someone")

    async def social_commands(self, ctx, search, top_x_gifs, string, binder, self_string, description, targets):
        if targets == []:
            await ctx.send(f"please specify who you want to {ctx.command.name}")
            return

        gif_count = top_x_gifs
        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s"
            % (f"anime gif {search}", tenor_api_key, gif_count)
        )
        actees = []
        for member in targets:
            if member.id not in actees:
                actees.append(member.id)

        title_string = f"{await SL.removeat(ctx.author.display_name)} {string} "

        if len(actees) == 1 and actees[0] == ctx.author.id:
            title_string = f"{await SL.removeat(ctx.author.display_name)} {self_string}"

        else:
            for i in range(0, len(actees)):
                if i >= len(actees) - 1 and i != 0:
                    title_string += f"and "
                person = await SL.removeat(self.bot.get_guild(ctx.guild.id).get_member(actees[i]).display_name)
                title_string += f"{person}, "

            title_string = title_string[:-2] + binder

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs["results"][random.randrange(0, gif_count)]["media"][0]["gif"]["url"]
            #print(realoutput)
            embed = Embed(title=title_string, description=description, colour=ctx.author.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)

            await ctx.send(embed=embed)
        
    @commands.command(name="bite", aliases=["rawr"], brief="rawr x3")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def bitecommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "bite", 30, "just bit", "", "just bit themselves... weirdo", "rawr", targets)
    
 
    @commands.command(name="tickle", brief="god you poor little thing")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def ticklecommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "tickle", 30, "just tickled", "", "just tickled themselves... pretty impressive", "teehee", targets)
    
    
    @commands.command(name="stare", aliases=["look"], brief="okay, creep")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def arsarsars(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "stare", 30, "is looking at", "", "is looking at themselves, how do you even do that? a mirror?", "peekaboo", targets)


    @commands.command(name="hold", aliases=["holdhands", "sex"], brief="aweeee :)")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def arsarsars(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "hold hands", 20, "is doing lewd things to", ", how cute", "discovered that holding hands with oneself is really just clapping when you think about it", "omggg so lewd", targets)


    @commands.command(name="cuddle", aliases=["hug²"], brief="it's like hugs, but even more wholesome")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def cuddlecommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "cuddle", 25, "took", ", forcing them to go <a:cuddle:888504653938044999>", "is hugging themselves, low key cute ngl 😊", "awwwweeee", targets)


    @commands.command(name="kiss", aliases=["smooch"], brief="awwweee :D")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def smooches(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "kiss", 25, "just kissed", ", and they're so cute!", "is somehow cute enough to kiss themselves?????+", "i ship it", targets)
        

    @commands.command(name="pat", aliases=["headpat", "pet"], brief="what if we pat eachother in public :fleeshed:")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def patpat(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "headpat", 25, "gave", " a big ol' headpat", "got a big pat from themselves, impressive", "pat pat", targets)
       #await self.social_commands(ctx, "headpat", 50, "gave", " gave2", "selfgive", "description", targets)   
        

    @commands.command(name="boop", aliases=["poke"], brief="make someone go bleep :)")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def boopcommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "boop", 20, "just forced", " to go bleep", "decided to bleep themselves, just cuz", "uwu", targets)


    @commands.command(name="punch", aliases=["hit"], brief="bit rude but o k")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def punchcommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "punch", 25, "hit", " ", "is punching, wait, why?", "at least it's not murder", targets)
        

    @commands.command(name="steal", aliases=["joink"], brief="mine now")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def stealcommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "steal", 25, "just stole something from ", "", "is trying to cheat the system", "don't steal my beavers >:(", targets)


    @commands.command(name="hug", aliases=["hugs"], brief="hugs :)")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def hugss(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "hug", 25, "hugged ", "", "do you need a hug? :(", "hugs :)", targets)
        

    @commands.command(name="fuck", brief="hi there, you found the hidden command")
    @cooldown(5, 25, BucketType.guild)
    @commands.guild_only()
    async def fuck_command(self, ctx, targets: Greedy[Member]):
        for person in targets:
            await ctx.send(f"hey {person.mention} do you consent to {ctx.author.mention} uhm.. yeah..")
            try:
                response = await self.bot.wait_for(
                    "message", check=lambda m: m.author == person, timeout=30
                )
            except asyncio.TimeoutError:
                return await ctx.send(await SL.removeat(f"**Timed out** {person.display_name} took too long to answer, cancelling"))
            if response.content.lower() not in confirmations:
                await ctx.send(f"yeah no, sorry {ctx.author.mention}, i'm not doing that :p")
                return
            
        await self.social_commands(ctx, "blush", 40, "did uh... something with", "", "is... enjoying themselves?!?", "woahwoahwaoh", targets)

    @commands.command(name="kill", aliases=["murder"], brief="that's an official oisann moment")
    @cooldown(8, 25, BucketType.guild)
    @commands.guild_only()
    async def killcommand(self, ctx, *, member: discord.Member):
        # not tenor, less graphical API
        api_url = "https://api.satou-chan.xyz/api/endpoint/kill"

        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["url"]

            else:
                image_link = None

        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                embed = Embed(
                    title=f"{await SL.removeat(ctx.author.display_name)} just murderified {await SL.removeat(member.display_name)}",
                    description="woah there",
                    colour=member.colour,
                )
                if image_link is not None:
                    embed.set_image(url=image_link)

                if ctx.author != member:
                    await ctx.send(embed=embed)

                if ctx.author == member:
                    lonely_embed = Embed(title=f"no.", colour=0xFF0000)
                    await ctx.send(embed=lonely_embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")


async def setup(bot):
    await bot.add_cog(social(bot))
