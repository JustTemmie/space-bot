import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import random
import libraries.standardLib as SL 
from datetime import datetime
from math import floor
class shipcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ship", brief="Ship two users :)")
    async def ship_command(self, ctx, person1: Member, person2: Member = "author"):
        if person2 == "author":
            person2 = person1
            person1 = ctx.author
        
        if person1 == person2:
            await ctx.send("Please don't give me two of the same user")
            return
        
        random.seed(person1.id + person2.id + floor((datetime.utcnow() - datetime(1970, 1, 1)).days / 20))
        await ctx.send(f"i give a ship between {await SL.removeat(person1.display_name)} and {await SL.removeat(person2.display_name)} a solid {random.randint(0, 100)} / 100")
        random.seed()
        


def setup(bot):
    bot.add_cog(shipcog(bot))
