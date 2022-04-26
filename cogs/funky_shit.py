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
        
    
    @commands.command(name = "beaver", brief = "reacts with beaver to the message corresponding with the ID you send\nALTERNATIVELY the bot will reac to the message you to using discord's built in reply feature")
    @cooldown(5, 10, BucketType.user)
    async def react_beaver_command(self, ctx, id = None):
        
        message = ctx.message
        await self.bot.http.delete_message(message.channel.id, message.id)

        if message.reference:
            id = message.reference.message_id
            message = await message.channel.fetch_message(id)
            await message.add_reaction("<a:Beaver:950775158552014928>")
            
        elif id != None:
            message = await message.channel.fetch_message(id)
            await message.add_reaction("<a:Beaver:950775158552014928>")
        
        else:
            await ctx.send(f"to use this command, reply to a message with {ctx.prefix}beaver", delete_after = 7)
        
    
    @commands.command(name = "unbeaver", brief = "beavern't")
    @cooldown(5, 10, BucketType.user)
    async def react_beaver_command(self, ctx, id = None):
        
        message = ctx.message
        await self.bot.http.delete_message(message.channel.id, message.id)

        if message.reference:
            id = message.reference.message_id
            message = await message.channel.fetch_message(id)
            await message.remove_reaction("<a:Beaver:950775158552014928>")
            
        elif id != None:
            message = await message.channel.fetch_message(id)
            await message.remove_reaction("<a:Beaver:950775158552014928>")
        
        else:
            await ctx.send(f"to use this command, reply to a message with {ctx.prefix}beaver", delete_after = 7)



def setup(bot):
    bot.add_cog(funky(bot))