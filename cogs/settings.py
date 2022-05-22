import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.settings import *


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        name="settings",
        aliases=["set", "config", "cfg"],
        brief="change settings for commands",
    )
    @cooldown(1, 2, BucketType.user)
    async def settingsCommand(self, ctx, command = "None", setting = "None", value = "None"):
        await store_user_id(ctx.author)
        
        if command == "None":
            await ctx.send(f"{ctx.prefix}settings <command> <setting> <value>")
            return

        data = await get_settings()
        if command.lower() in ["trivia", "triv", "quiz"]:
            try:
                data[str(ctx.author.id)]["trivia"]
            except:
                data[str(ctx.author.id)]["trivia"] = {}
            
            embed = discord.Embed(title="Trivia Settings", color=ctx.author.color)
            embed.set_footer(text=f"{ctx.author} | {ctx.prefix}settings trivia <setting> <value>")
            
            embed.add_field(name="Test", value="True, False, Both", inline=False)
            await ctx.send(embed = embed)
                
        
        if data != await get_settings():
            with open("storage/user/settings.json", "w") as f:
                json.dump(data, f)
            return
        
        await ctx.send("i could not find any settings for that command")


def setup(bot):
    bot.add_cog(settings(bot))
