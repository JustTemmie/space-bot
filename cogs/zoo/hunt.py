import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


import libraries.animalLib as aniLib


class ecobuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="hunt",
        brief="go look for some animals, perhaps even add them to your zoo"
    )
    @cooldown(2, 10, BucketType.user)
    async def huntCommand(self, ctx):
        await aniLib.open_zoo(self, ctx)
        
        if await aniLib.check_if_zoo_not_exist(ctx.author):
            return await ctx.send("you need to create an account first")
        
        with open("storage/animals.json", "r") as f:
            animals = json.load(f)
        
        data = await aniLib.get_animal_data()
        
        for i in animals:
            #await ctx.send(animals(i)["name"])
            for y in range(1, 7):
                await ctx.send(animals[i]["animals"][str(y)]["icon"])
                await ctx.send(animals[i]["animals"][str(y)]["name"][0])
    
def setup(bot):
    bot.add_cog(ecobuild(bot))
