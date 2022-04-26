import discord
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, Greedy, CheckFailure, command, has_permissions, bot_has_permissions
import json

import time

       
        
class marry(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "marry")
    async def react_henwee(self, ctx, member:discord.Member):
        await ctx.send("{} is now married to {}".format(ctx.author.mention, member.mention))
        time.sleep(5)

        await ctx.send("lmao yea as if i'm not storing that too much effort")

def setup(bot):
    bot.add_cog(marry(bot))