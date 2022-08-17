import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


import requests
from libraries.economyLib import *
import libraries.standardLib as SL 

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
tenor_api_key = os.getenv("TENOR")

class stickyummy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eat", aliases=["nom"], brief="yummy")
    @cooldown(1, random.randint(500, 750), BucketType.user)
    @commands.guild_only()
    async def eatcommand(self, ctx):
        await open_account(self, ctx)
        
        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send(f"i could not find your inventory, they need to create an account first")
    
        bank = await get_bank_data()
        
        if bank[str(ctx.author.id)]["inventory"]["stick"] >= 1:
        
            r = requests.get(
                "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s"
                % (f"anime eat stick", tenor_api_key, 30)
            )

            if r.status_code == 200:
                top_x_gifs = json.loads(r.content)
                realoutput = top_x_gifs["results"][random.randrange(0, 30)]["media"][0]["gif"]["url"]
                #print(realoutput)
                embed = Embed(title=f"{await SL.removeat(ctx.author.display_name)} ate a stick", description="nomch", colour=ctx.author.colour)
                if realoutput is not None:
                    embed.set_image(url=realoutput)

                with open("./storage/playerInfo/bank.json", "r") as f:
                    data = json.load(f)
                    
                data[str(ctx.author.id)]["inventory"]["stick"] -= 1
                data[str(ctx.author.id)]["statistics"]["total_sticks_eaten"] += 1
                
                print(data)
                
                with open("./storage/playerInfo/bank.json", "w") as f:
                    json.dump(data, f)
                    
                await ctx.send(embed=embed)
                
                
                return
            
            await ctx.send("an error occured, sorry about that")
            return
        
        await ctx.send(f"you don't have any sticks to eat, get some by looking into the `{ctx.prefix}shop`")
        


async def setup(bot):
    await bot.add_cog(stickyummy(bot))
