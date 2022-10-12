from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import random

import libraries.animalLib as aniLib
import libraries.economyLib as ecoLib
from libraries.captchaLib import *
from libraries.standardLib import removeat

tiers = {
    # chance of finding an animal, from 0 to 1 where 1 is 100%
    "legendary": 0.0001,
    "mythical": 0.001,
    "epic": 0.01,
    "rare": 0.05,
    "uncommon": 0.2,
    "common": 1,
}

class zooHunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
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

        animals_to_get = 1
        caught = []
        caughttier = []
        
        # skills
        chance_for_bonus = 0
        if bank[str(ctx.author.id)]["lodge"]["level"] >= 1:
            chance_for_bonus = 0.2
        if bank[str(ctx.author.id)]["lodge"]["level"] >= 2:
            chance_for_bonus += 0.3
        if bank[str(ctx.author.id)]["lodge"]["level"] >= 3:
            chance_for_bonus += 0.5

        if random.random() <= chance_for_bonus:
            animals_to_get += 1

                
        for i in range(0, animals_to_get):
            animal, tier = await self.roll_animal(ctx, animals)
            caught.append(animal)
            caughttier.append(tier)


        if len(caught) == 1:
            await ctx.send(f"{await removeat(ctx.author.display_name)}, you went on a hunt and caught a {caught[0]['name'][0]} {caught[0]['icon']}, it's {animals[caughttier[0]]['aoran']} {caughttier[0]}{animals[caughttier[0]]['icon']} animal")
        else:
            peak_rarity = ""
            peak_animal = ""
            for i, animal in enumerate(caught):
                if caughttier[i] not in ["common", "uncommon", "rare"]:
                    for n in tiers:
                        if peak_rarity == n:
                            break
                        if caughttier[i] == n:
                            peak_rarity = n
                            peak_animal = animal["name"][0]
                            break
            
            animalIcons = ""
            for i in range(0, len(caught)):
                animalIcons += caught[i]["icon"] + " "
                
            bonusStr = ""
            if peak_rarity != "":
                bonusStr = f"\nwoah, that {peak_animal}... it's {animals[peak_rarity]['aoran']} {peak_rarity}{animals[peak_rarity]['icon']}animal"
            
            await ctx.send(f"{await removeat(ctx.author.display_name)} went on a hunt\nThey found: {animalIcons}{bonusStr}")

        
        data = await aniLib.get_animal_data()
        
        for i, n in zip(caught, caughttier):
            data[str(ctx.author.id)]["animals"][n][i["name"][0]]["caught"] += 1
            data[str(ctx.author.id)]["animals"][n][i["name"][0]]["count"] += 1
            
            data["global"]["animals"][n][i["name"][0]]["caught"] += 1
            with open("storage/playerInfo/animals.json", "w") as f:
                json.dump(data, f)#, indent=4)


    async def roll_animal(self, ctx, animals):
        roll = random.random()
        discarded_roll = 0
        for tier in tiers:
            if tiers[tier]+discarded_roll > roll:
                break
            discarded_roll += round(tiers[tier], 3)
        
        ID = random.randint(1, 6)
        
        selectedAnimal = animals[tier]["animals"][str(ID)]
        
        return selectedAnimal, tier
    
async def setup(bot):
    await bot.add_cog(zooHunt(bot))
