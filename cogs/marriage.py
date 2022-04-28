import discord
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, Greedy, CheckFailure, command, has_permissions, bot_has_permissions
import json

import time

       
        
class marriage(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "marry")
    async def react_henwee(self, ctx, member:discord.Member):
        if member == None:
            await ctx.send("please give me a member to marry")
            return
        
        await ctx.send(f"you do not have any rings to give {member.mention}", delete_after = 20)
        return
            
        await ctx.send("{} is now married to {}".format(ctx.author.mention, member.mention), delete_after = 15)
        time.sleep(5)

        await ctx.send("lmao yea as if i'm not storing that too much effort", delete_after = 15)

def setup(bot):
    bot.add_cog(marriage(bot))