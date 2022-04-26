import discord
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, Greedy, CheckFailure, command, has_permissions, bot_has_permissions
import json


       
        
class marry(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    


def setup(bot):
    bot.add_cog(marry(bot))