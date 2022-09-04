from os import dup
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import random

import libraries.animalLib as aniLib
import libraries.economyLib as ecoLib
from libraries.captchaLib import *

tiers = {
    # chance of finding an animal, from 0 to 1 where 1 is 100%
    "legendary": 0.00015,
    "mythical": 0.001,
    "epic": 0.01,
    "rare": 0.05,
    "uncommon": 0.2,
    "common": 1,
}

class zooHunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name = "hunt",
        aliases = ["hu"],
        brief = "go look for some animals, perhaps even add them to your zoo"
    )
    @cooldown(1, 300, BucketType.user)
    async def huntCommand(self, ctx):
        await ecoLib.open_account(self, ctx)
        await aniLib.open_zoo(self, ctx)
                
        userNotExist = await aniLib.check_if_zoo_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        if await check_captcha(self, ctx, 1.2):
            return

        bank = await ecoLib.get_bank_data()
        animals = await aniLib.get_zoo_data()

        
        selectedAnimal, animal_name, tier = await self.roll_animal(ctx, animals)
        
        
        # skills
        animalmulti = 0
        animal2 = animal2name = tier2 = ""
        if bank[str(ctx.author.id)]["lodge"]["level"] >= 1:
            animalmulti += 1
        if bank[str(ctx.author.id)]["lodge"]["level"] >= 2:
            animalmulti += 1.5
        if bank[str(ctx.author.id)]["lodge"]["level"] >= 3:
            animalmulti += 2.5

        if random.random() < 0.20 * animalmulti:
            animal2, animal2name, tier2 = await self.roll_animal(ctx, animals)

        
        if animal2 == "":
            await ctx.send(f"You caught a {animal_name} {selectedAnimal['icon']}, it's {animals[tier]['aoran']} {tier}{animals[tier]['icon']} animal")
        else:
            duplicatestr = "a"
            if animal2name == animal_name:
                duplicatestr = "another"
            await ctx.send(f"You caught a {animals[tier]['icon']} {animal_name} {selectedAnimal['icon']} and {duplicatestr} {animals[tier2]['icon']} {animal2name} {animal2['icon']}")

        
        data = await aniLib.get_animal_data()
        
        
        data[str(ctx.author.id)]["animals"][tier][animal_name]["caught"] += 1
        data[str(ctx.author.id)]["animals"][tier][animal_name]["count"] += 1
        
        data["global"]["animals"][tier][animal_name]["caught"] += 1
        
        if animal2 != "":
            data[str(ctx.author.id)]["animals"][tier2][animal2name]["caught"] += 1
            data[str(ctx.author.id)]["animals"][tier2][animal2name]["count"] += 1
            
            data["global"]["animals"][tier2][animal2name]["caught"] += 1

        with open("storage/playerInfo/animals.json", "w") as f:
            json.dump(data, f)#, indent=4)
        
        # for i in animals:
        #     #await ctx.send(animals(i)["name"])
        #     for y in range(1, 7):
        #         await ctx.send(animals[i]["animals"][str(y)]["icon"])
        #         await ctx.send(animals[i]["animals"][str(y)]["name"][0])

    async def roll_animal(self, ctx, animals):
        roll = random.random()
        for tier in tiers:
            if tiers[tier] > roll:
                break
        
        ID = random.randint(1, 6)
        
        selectedAnimal = animals[tier]["animals"][str(ID)]
        animal_name = selectedAnimal["name"][0]
        
        return selectedAnimal, animal_name, tier
    
async def setup(bot):
    await bot.add_cog(zooHunt(bot))
