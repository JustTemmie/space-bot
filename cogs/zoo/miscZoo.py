import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


import  libraries.economyLib as ecoLib
import  libraries.animalLib as aniLib


class miscZoo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="zoo", brief="zoo")
    @cooldown(2, 10, BucketType.user)
    async def checkZoo(self, ctx, input = None):
        with open("storage/animals.json", "r") as f:
            zoo = json.load(f)
        
        await aniLib.open_zoo(ctx.author)

        if input == None:
            message_str = ""
            
            for tier in zoo:
                message_str += str(zoo[tier]["icon"])
                for i in zoo[tier]["animals"]:
                    animal = zoo[tier]["animals"][i]
                    icon = animal["icon"]
                    name = animal["name"][0]
                    message_str += f"{icon} "
                message_str += f"\n"
            
            await ctx.send(message_str)
            return
        
        input = input.lower()
        animalName = "none"
        for tier in zoo:
            for i in zoo[tier]["animals"]:
                animal = zoo[tier]["animals"][i]
                for nick in range(0, len(animal["name"])):
                    if input == animal["name"][nick]:
                        icon = animal["icon"]
                        animalName = animal["name"][0]
                        break
        
        if animalName == "none":
            return await ctx.send(f"{input} was not found")
        
        embed = discord.Embed()
        embed.title = f"{icon} {animalName}"
        embed.color = ctx.author.colour
        embed.description = "   Can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        
        embed.add_field(
            inline=False,
            name="||\n||",
            value=f"""
**Tier:** {zoo[tier]["icon"]} {zoo[tier]["name"]}
**Caught:** 2
another test
            """)
        
        await ctx.send(embed=embed)
        
        

def setup(bot):
    bot.add_cog(miscZoo(bot))
