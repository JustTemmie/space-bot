import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions
import ast
import sys
import os
import subprocess

class owner_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    

def setup(bot):
    bot.add_cog(owner_events(bot))