import discord
from discord import Member, File, Embed, Intents, Object, NotFound
from discord.errors import HTTPException, Forbidden
from discord.utils import find
from discord.ext import tasks, commands
from discord.ext.commands import (
    cooldown,
    BucketType,
    Greedy,
    MissingRequiredArgument,
)

import json
from aiohttp import request
import random
import requests

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
tenor_api_key = os.getenv("TENOR")


class social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name="rape", aliases=["sex", "r4pe", "r4p3", "rap3", "epar", "pare", "reap", "raape", "raaape", "raaaape", "rapee"], hidden = True)
    # async def rapeisbad(self, ctx, member:discord.Member):
    #    member = ctx.author
    #    await ctx.send(f"{ctx.author} tried to rape someone, to stop this from happening in the future they have been kicked from the server")
    #    await member.kick(reason="tried to rape someone")

    async def social_commands(self, ctx, search, top_x_gifs, string, binder, self_string, description, targets):
        gif_count = top_x_gifs
        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s"
            % (f"anime gif {search}", tenor_api_key, gif_count)
        )
        actees = []
        for member in targets:
            if member.id not in actees:
                actees.append(member.id)

        title_string = f"{ctx.author.display_name} {string} "

        if len(actees) == 1 and actees[0] == ctx.author.id:
            title_string = f"{ctx.author.display_name} {self_string}"

        else:
            for i in range(0, len(actees)):
                if i >= len(actees) - 1 and i != 0:
                    title_string += f"and "
                person = self.bot.get_guild(ctx.guild.id).get_member(actees[i]).display_name
                title_string += f"{person}, "

            title_string = title_string[:-2] + binder

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs["results"][random.randrange(0, gif_count)]["media"][0]["gif"][
                "url"
            ]
            print(realoutput)
            embed = Embed(title=title_string, description=description, colour=ctx.author.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)

            await ctx.send(embed=embed)
        
    @commands.command(name="bite", aliases=["rawr"], brief="rawr x3")
    @cooldown(8, 25, BucketType.guild)
    async def bitecommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "bite", 50, "just bit", "", "just bit themselves... weirdo", "rawr", targets)
        
        
        # gif_count = 50
        # r = requests.get(
        #     "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s"
        #     % ("anime gif bite", tenor_api_key, gif_count)
        # )

        # actees = []
        # for member in targets:
        #     if member.id not in actees:
        #         actees.append(member.id)

        # title_string = f"{ctx.author.display_name} just bit "

        # if len(actees) == 1 and actees[0] == ctx.author.id:
        #     title_string = f"{ctx.author.display_name} just bit themselves... weirdo"

        # else:
        #     for i in range(0, len(actees)):
        #         if i >= len(actees) - 1 and i != 0:
        #             title_string += f"and "
        #         person = self.bot.get_guild(ctx.guild.id).get_member(actees[i]).display_name
        #         title_string += f"{person}, "

        #     title_string = title_string[:-2]

        # if r.status_code == 200:
        #     top_x_gifs = json.loads(r.content)
        #     realoutput = top_x_gifs["results"][random.randrange(0, gif_count)]["media"][0]["gif"][
        #         "url"
        #     ]
        #     print(realoutput)
        #     embed = Embed(title=title_string, description="rawr", colour=ctx.author.colour)
        #     if realoutput is not None:
        #         embed.set_image(url=realoutput)

        #     await ctx.send(embed=embed)
    
    
    @commands.command(name="tickle", brief="god you poor little thing")
    @cooldown(8, 25, BucketType.guild)
    async def ticklecommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "tickle", 30, "just tickled", "", "just tickled themselves... pretty impressive", "teehee", targets)         


    @commands.command(
        name="cuddle",
        aliases=["hug²"],
        brief="it's like hugs, but ever more wholesome",
    )
    @cooldown(8, 25, BucketType.guild)
    async def cuddlecommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "cuddle", 25, "took", ", forcing them to go <a:cuddle:888504653938044999>", "is hugging themselves, low key cute ngl 😊", "awwwweeee", targets)         
        

    @commands.command(name="kill", aliases=["murder"], brief="that's an official oisann moment")
    @cooldown(8, 25, BucketType.guild)
    async def killcommand(self, ctx, *, member: discord.Member):
        # not tenor
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
                    title=f"{ctx.author.display_name} just murderified {member.display_name}",
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

    @commands.command(name="kiss", aliases=["smooch"], brief="awwweee :D")
    @cooldown(8, 25, BucketType.guild)
    async def smooches(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "kiss", 50, "just kissed", ", and they're so cute!", "is somehow cute enough to kiss themselves?????+", "i ship it", targets)   
        

    @commands.command(
        name="pat",
        aliases=["headpat", "pet"],
        brief="what if we pat eachother in public :fleeshed:",
    )
    @cooldown(8, 25, BucketType.guild)
    async def patpat(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "headpat", 50, "gave", " a big ol' headpat", "got a big pat from themselves, impressive", "pat pat", targets)   
        await self.social_commands(ctx, "headpat", 50, "gave", " gave2", "selfgive", "description", targets)   
        

    @commands.command(name="boop", aliases=["poke"], brief="make someone go bleep :)")
    @cooldown(8, 25, BucketType.guild)
    async def boopcommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "boop", 20, "just forced", " to go bleep", "decided to bleep themselves, just cuz", "uwu", targets)


    @commands.command(name="punch", aliases=["hit"], brief="bit rude but o k")
    @cooldown(8, 25, BucketType.guild)
    async def punchcommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "punch", 50, "hit", " ", "is punching, wait, why?", "at least it's not murder", targets)   
        

    @commands.command(name="steal", aliases=["joink"], brief="mine now")
    @cooldown(8, 25, BucketType.guild)
    async def stealcommand(self, ctx, targets: Greedy[Member]):
        await self.social_commands(ctx, "steal", 50, "just stole something from ", "", "is trying to cheat the system", "don't steal my beavers >:(", targets)   
        


    @commands.command(name="hug", aliases=["hugs"], brief="hugs :)")
    @cooldown(8, 25, BucketType.guild)
    async def hugss(self, ctx, *, member: discord.Member):
        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s"
            % ("anime gif hug", tenor_api_key, 50)
        )

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs["results"][random.randrange(0, 50)]["media"][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(
                title=f"{ctx.author.display_name} hugged {member.display_name}",
                description=":)",
                colour=ctx.author.colour,
            )
            if realoutput is not None:
                embed.set_image(url=realoutput)

            if ctx.author == member:
                lonely_embed = Embed(
                    title=f"{ctx.author.display_name}, do you need a hug? :(",
                    colour=ctx.author.colour,
                )
                if realoutput is not None:
                    lonely_embed.set_image(url=realoutput)
                await ctx.send(embed=lonely_embed)

            else:
                await ctx.send(embed=embed)

    @commands.command(name="grouphug", aliases=["multihug"], brief="hugs :)")
    @cooldown(8, 25, BucketType.guild)
    async def multihugz(self, ctx, targets: Greedy[Member]):
        if not len(targets):
            await ctx.send("One or more of the required arguments are missing")

        else:
            users = []
            n = 0
            for target in targets:
                users.append(target.display_name)

        bad_chars = ["'", '"']
        for i in bad_chars:
            users = str(users).replace(i, "")

        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s"
            % ("anime gif group hug", tenor_api_key, 50)
        )

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs["results"][random.randrange(0, 50)]["media"][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(
                title=f"{(str(users)[1:-1])}, and {ctx.author.display_name} all got together for a big group hug",
                description=":)",
                colour=ctx.author.colour,
            )
            if realoutput is not None:
                embed.set_image(url=realoutput)

            await ctx.send(embed=embed)

        else:
            await ctx.send(
                f"i couldn't seem to find anything related to `group hug` or the API fucking died, i dunnu"
            )


def setup(bot):
    bot.add_cog(social(bot))
