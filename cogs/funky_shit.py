import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

class funky(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name = "ai", brief = "give an ai a input string and it will return... something :)")
    @cooldown(5, 10, BucketType.user)
    async def ai_command(self, ctx):
        await ctx.send("lmao no")
        
    
    @commands.command(name = "beaver", brief = "reacts with beaver to the last message sent\nalternatively it will react with beaver to the message you reply to")
    @cooldown(5, 10, BucketType.user)
    async def react_beaver_command(self, ctx):
        
        message = ctx.message
        await self.bot.http.delete_message(message.channel.id, message.id)

        if message.reference:
            print(message)
            id = message.reference.message_id
            message = await message.channel.fetch_message(id)
            await message.add_reaction("🦫")
        
        else:
            await ctx.send(f"to use this command, reply to a message with {ctx.prefix}beaver", delete_after = 7)
        
        



def setup(bot):
    bot.add_cog(funky(bot))