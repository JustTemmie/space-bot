import discord
from discord import Member, Embed
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
import json



class reminderTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        reminderTask.start()

    @tasks.loop(seconds=10)
    async def reminderTask(self):
        pass
        # do stuff :)

def setup(bot):
    bot.add_cog(reminderTask(bot))
