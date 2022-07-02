from collections import UserList
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import libraries.animalLib as aniLib


class miscZoo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        name="zoo",
        brief="check your zoo"
    )
    @cooldown(2, 10, BucketType.user)
    async def checkZoo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
            
        await aniLib.open_zoo(self, ctx)
        
        if await aniLib.check_if_zoo_not_exist(user):
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        with open("storage/animals.json", "r") as f:
            zoo = json.load(f)
        
        data = await aniLib.get_animal_data()
        

        end = "s"
        if user.display_name[-1:] == "s":
            end = ""
        message_str = f"||\n||                  🌲  **{user.display_name}'{end} zoo:**  🌲\n\n"
        
        animalsInTiers = {
            "common": [],
            "uncommon": [],
            "rare": [],
            "epic": [],
            "mythical": [],
        }

        for tier in zoo:
            for i in zoo[tier]["animals"]:
                animal = zoo[tier]["animals"][i]
                icon = animal["icon"]
                name = animal["name"][0]
                caught = data[str(user.id)]['animals'][tier][name]["caught"]
                if caught != 0 or tier == "common":
                    animalsInTiers[tier].append(f"{icon}`{data[str(user.id)]['animals'][tier][name]['count']}` ")

        for tier in animalsInTiers:
            if len(animalsInTiers[tier]) != 0:
                message_str += f"{zoo[tier]['icon']}    {' '.join(animalsInTiers[tier])}\n"
                        
        await ctx.send(message_str)
        return
    
    @commands.command(
        name="dex",
        brief="check a specific animal"
    )
    @cooldown(3, 10, BucketType.user)
    async def dexCommand(self, ctx, input, user: discord.Member = None):
        input = input.lower()
        await aniLib.open_zoo(self, ctx)
        
        if user is None:
            user = ctx.author

        if await aniLib.check_if_zoo_not_exist(ctx.author):
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        with open("storage/animals.json", "r") as f:
            zoo = json.load(f)
        
        data = await aniLib.get_animal_data()
        
        
        animalName = "none"
        for tier in zoo:
            for i in zoo[tier]["animals"]:
                animal = zoo[tier]["animals"][i]
                for nick in range(0, len(animal["name"])):
                    if input == animal["name"][nick]:
                        icon = animal["icon"]
                        animalName = animal["name"][0]
                        names = ""
                        for name in animal["name"]:
                            names += f"{name}, "
                        animalTier = tier
                        break
        
        if animalName == "none":
            return await ctx.send(f"{input} was not found")
        
        if data[str(user.id)]["animals"][animalTier][animalName]["caught"] == 0:
            return await ctx.send(f"{input} was not found")

 
        embed = discord.Embed()
        embed.title = f"{icon} {animalName}"
        embed.color = user.colour
        #embed.description = f"{animalTier}"
        #embed.description = "   Can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        
        aliasesString = ""
        if len(names[(len(animalName)+2):-2]) >= 1:
            aliasesString = f"\n**AKA:** {names[(len(animalName)+2):-2]}"
        
        embed.add_field(
            inline=False,
            name="||\n||",
            value=f"""
**Tier:** {zoo[animalTier]["icon"]} {animalTier}{aliasesString}
**Caught:** {data[str(user.id)]["animals"][animalTier][animalName]["caught"]}
**Total Caught:** {data["global"]["animals"][animalTier][animalName]["caught"]}
**Count:** {data[str(user.id)]["animals"][animalTier][animalName]["count"]}
**Sold:** {data[str(user.id)]["animals"][animalTier][animalName]["sold"]}
**Sacrificed:** {data[str(user.id)]["animals"][animalTier][animalName]["sacrificed"]}
**XP:** {data[str(user.id)]["animals"][animalTier][animalName]["xp"]}
            """)
        
        await ctx.send(embed=embed)
        
        

def setup(bot):
    bot.add_cog(miscZoo(bot))
