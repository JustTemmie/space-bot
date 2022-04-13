import discord
from discord.ext import commands

class suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.channel.id == (919609742542897242):
                await message.add_reaction("👍")
                await message.add_reaction("👎")
                
        except:
            pass

def setup(bot):
    bot.add_cog(suggestions(bot))