import discord
from discord import Member, File, Embed, Intents, Object, NotFound
from discord.errors import HTTPException, Forbidden
from discord.utils import find
from discord.ext import tasks, commands
from discord.ext.commands import cooldown, BucketType, CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, when_mentioned_or, command, has_permissions, bot_has_permissions, Greedy, Converter, CheckFailure, Cog, MissingRequiredArgument

import json
from aiohttp import request
import random
import requests

import os
from dotenv import load_dotenv
load_dotenv("TENOR_API_KEY.env")
tenor_api_key = os.getenv("KEY")


class social(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rape", aliases=["sex", "r4pe", "r4p3", "rap3", "epar", "pare", "reap", "raape", "raaape", "raaaape", "rapee"], hidden = True)
    async def rapeisbad(self, ctx, member:discord.Member):
        member = ctx.author
        await ctx.send(f"{ctx.author} tried to rape someone, to stop this from happening in the future they have been kicked from the server")
        await member.kick(reason="tried to rape someone")


    @commands.command(name="bite", aliases=["rawr"], brief="rawr x3")
    @cooldown(8, 25, BucketType.guild)
    async def bitecommand(self, ctx, targets: Greedy[Member]):
        gif_count = 50
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime gif bite", tenor_api_key, gif_count))

        
        actees = []
        for member in targets:
            if member.id not in actees:
                actees.append(member.id)
        
        kiss_string = f"{ctx.author.display_name} just bit "
        
        if len(actees) == 1 and actees[0] == ctx.author.id:
            kiss_string = f"{ctx.author.display_name} just bit themselves... weirdo"
        
        else:
            for i in range(0, len(actees)):
                if i >= len(actees) - 1 and i != 0:
                    kiss_string += f"and "
                person = self.bot.get_guild(ctx.guild.id).get_member(actees[i]).display_name
                kiss_string += f"{person}, "

        
        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, gif_count)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=kiss_string[:-2],
                              description="rawr",
                              colour=ctx.author.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            await ctx.send(embed=embed)

      
    @commands.command(name="cuddle", aliases=["hug^2"], brief="it\'s like hugs, but ever more wholesome")
    @cooldown(8, 25, BucketType.guild)
    async def cuddlecommand(self, ctx, targets: Greedy[Member]):
        gif_count = 25
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime gif cuddle", tenor_api_key, gif_count))

        
        actees = []
        for member in targets:
            if member.id not in actees:
                actees.append(member.id)
        
        kiss_string = f"{ctx.author.display_name} took "
        
        if len(actees) == 1 and actees[0] == ctx.author.id:
            kiss_string = f"{ctx.author.display_name} is hugging themselves, low key cute ngl+"
        
        else:
            for i in range(0, len(actees)):
                if i >= len(actees) - 1 and i != 0:
                    kiss_string += f"and "
                person = self.bot.get_guild(ctx.guild.id).get_member(actees[i]).display_name
                kiss_string += f"{person}, "

        
        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, gif_count)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=kiss_string[:-2] + ", forcing them to go <a:cuddle:888504653938044999>",
                              description="awweeee",
                              colour=ctx.author.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            await ctx.send(embed=embed)


    @commands.command(name="kill", aliases=["murder"], brief="that's an official oisann moment")
    @cooldown(8, 25, BucketType.guild)
    async def killcommand(self, ctx, *, member:discord.Member):
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
                            
                embed = Embed(title=f"{ctx.author.display_name} just murderified {member.display_name}",
                              description="woah there",
                              colour=member.colour)
                if image_link is not None:
                    embed.set_image(url=image_link)
                
                if ctx.author  != member:
                    await ctx.send(embed=embed)
                
                if ctx.author == member:
                    lonely_embed = Embed(title=f"no.",
                    colour = 0xff0000)
                    await ctx.send(embed=lonely_embed)
                        
            else:
                await ctx.send(f"API returned a {response.status} status.")

      
      
  
    @commands.command(name="kiss", aliases=["smooch"], brief="awwweee :D")
    @cooldown(8, 25, BucketType.guild)
    async def smooches(self, ctx, targets: Greedy[Member]):
        gif_count = 50
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime gif kiss", tenor_api_key, gif_count))

        actees = []
        for member in targets:
            if member.id not in actees:
                actees.append(member.id)
        
        kiss_string = f"{ctx.author.display_name} just kissed "
        
        if len(actees) == 1 and actees[0] == ctx.author.id:
            kiss_string = f"{ctx.author.display_name} is somehow cute enough to kiss themselves?????+"""
        
        else:
            for i in range(0, len(actees)):
                if i >= len(actees) - 1 and i != 0:
                    kiss_string += f"and "
                person = self.bot.get_guild(ctx.guild.id).get_member(actees[i]).display_name
                kiss_string += f"{person}, "

        
        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, gif_count)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=kiss_string[:-2],
                              description="i ship it",
                              colour=ctx.author.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            await ctx.send(embed=embed)


    @commands.command(name="pat", aliases=["headpat","pet"], brief="what if we pat eachother in public :fleeshed:")
    @cooldown(8, 25, BucketType.guild)
    async def patpat(self, ctx, *, member:discord.Member):
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime gif headpat", tenor_api_key, 50))

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, 50)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=f"{ctx.author.display_name} gave {member.display_name} a big o\'l pat",
                              description=":)",
                              colour=member.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            if ctx.author == member:
                lonely_embed = Embed(title=f"{ctx.author.display_name} got a big pat from themselves, impressive",
                    colour = ctx.author.colour)
                if realoutput is not None:
                    lonely_embed.set_image(url=realoutput)
                await ctx.send(embed=lonely_embed)
            
            else:
                await ctx.send(embed=embed)


    @commands.command(name="boop", aliases=["poke"], brief="make someone go bleep :)")
    @cooldown(8, 25, BucketType.guild)
    async def boopcommand(self, ctx, *, member:discord.Member):
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime boop", tenor_api_key, 10))

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, 10)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=f"{ctx.author.display_name} just forced {member.display_name} to go bleep",
                              description="uwu",
                              colour=member.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            if ctx.author == member:
                lonely_embed = Embed(title=f"{ctx.author.display_name} decided to bleep just cuz",
                colour = ctx.author.colour)
                if realoutput is not None:
                    lonely_embed.set_image(url=realoutput)
                await ctx.send(embed=lonely_embed)
                
            else:
                await ctx.send(embed=embed)


    
    @commands.command(name="punch", aliases=["hit"], brief="bit rude but o k")
    @cooldown(8, 25, BucketType.guild)
    async def punchcommand(self, ctx, *, member:discord.Member):
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime gif punch", tenor_api_key, 50))

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, 50)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=f"{ctx.author.display_name} hit {member.display_name}",
                              description="at least it\'s not murder",
                              colour=member.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            if ctx.author == member:
                    lonely_embed = Embed(title=f"{ctx.author.display_name} is uhm, punching themselves?",
                    colour = ctx.author.colour)
                    if realoutput is not None:
                        lonely_embed.set_image(url=realoutput)
                    await ctx.send(embed=lonely_embed)
            
            else:
                await ctx.send(embed=embed)


    @commands.command(name="steal", aliases=["joink"], brief="mine now")
    @cooldown(8, 25, BucketType.guild)
    async def stealcommand(self, ctx, *, member:discord.Member):
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime steal", tenor_api_key, 50))

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, 50)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=f"{ctx.author.display_name} just stole something from {member.display_name}",
                            description="at least it\'s not murder Â¯\_(ã)_/Â¯",
                            colour=member.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            if ctx.author == member:
                    lonely_embed = Embed(title=f"i think {ctx.author.display_name} is trying to cheat the system",
                    description="you can\'t just steal from yourself???",
                    colour = ctx.author.colour)
                    if realoutput is not None:
                        lonely_embed.set_image(url=realoutput)
                    await ctx.send(embed=lonely_embed)
            
            else:
                await ctx.send(embed=embed)


    
    @commands.command(name="hug", aliases=["hugs"], brief="hugs :)")
    @cooldown(8, 25, BucketType.guild)
    async def hugss(self, ctx, *, member:discord.Member):
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime gif hug", tenor_api_key, 50))

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, 50)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=f"{ctx.author.display_name} hugged {member.display_name}",
                            description=":)",
                            colour=ctx.author.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
                
            if ctx.author == member:
                    lonely_embed = Embed(title=f"{ctx.author.display_name}, do you need a hug? :(",
                    colour = ctx.author.colour)
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
        
        bad_chars = ['\'', "\""]
        for i in bad_chars :
            users = str(users).replace(i, '')
        
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("anime gif group hug", tenor_api_key, 50))

        if r.status_code == 200:
            top_x_gifs = json.loads(r.content)
            realoutput = top_x_gifs['results'][random.randrange(0, 50)]['media'][0]["gif"]["url"]
            print(realoutput)
            embed = Embed(title=f"{(str(users)[1:-1])}, and {ctx.author.display_name} all got together for a big group hug",
                            description=":)",
                            colour=ctx.author.colour)
            if realoutput is not None:
                embed.set_image(url=realoutput)
            
            await ctx.send(embed=embed)
            
        else:
            await ctx.send(f"i couldn\'t seem to find anything related to `group hug` or the API fucking died, i dunnu")
            



def setup(bot):
    bot.add_cog(social(bot))
