import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import random
from math import floor
from typing import Optional


import libraries.economyLib as ecoLib
import libraries.animalLib as aniLib


class ecoshop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="shop",
        aliases=["market"],
        brief="buy something, wouldya?"
    )
    @cooldown(5, 12, BucketType.user)
    async def shop_command(self, ctx, page=1):
        pages = 2
        if page > pages or page <= 0:
            await ctx.send("that page doesn't exist, sorry")
            return

        await ecoLib.open_account(self, ctx)
        
        userNotExist = await ecoLib.check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        shop = await ecoLib.get_shop_data()

        page_bonus_string = {1: "", 2: "**Rings:**\nUse them to marry someone\n"}[page]

        desc = f"Buy something, wouldya?\n\n{page_bonus_string}\n"
        for i in shop:
            if shop[i][2] == page:
                desc += f"{shop[i][1]} `{i}` {shop[i][4]}| {shop[i][0]} <:beaverCoin:968588341291397151>\n{shop[i][3]}"

        embed = discord.Embed(title="🛍 The Market", description=f"{desc}", colour=ctx.author.colour)
        embed.set_footer(text=f"Use {ctx.prefix}buy <item> to buy something\npage {page}/{pages}")

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="buy",
        aliases=["transact"],
        brief="pay for something, wouldya?"
    )
    @cooldown(5, 15, BucketType.user)
    async def buy_command(self, ctx, item, amount: Optional[int] = 1):
        await ecoLib.open_account(self, ctx)

        userNotExist = await ecoLib.check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        shop = await ecoLib.get_shop_data()
        bank = await ecoLib.get_bank_data()
        wallet = bank[str(ctx.author.id)]["wallet"]

        for i in shop:
            if item.lower() == i.lower():
                if wallet < (shop[i][0]) * amount:
                    await ctx.send("you don't have enough money to buy that many")
                    return

                try:
                    bank[str(ctx.author.id)]["inventory"][item.lower()] += 1 * amount
                except:
                    bank[str(ctx.author.id)]["inventory"][item.lower()] = 1 * amount

                bank[str(ctx.author.id)]["wallet"] -= shop[i][0] * amount

                with open("storage/playerInfo/bank.json", "w") as f:
                    json.dump(bank, f)

                await ctx.send(
                    f"You just bought {amount} {shop[i][1]} for {shop[i][0] * amount} <:beaverCoin:968588341291397151>"
                )
                return

        await ctx.send("i could not find that item, sorry")
        
    
    @commands.command(
        name="sell",
        brief="try selling your animals for money\nyou can sell a specific animal, an entire tier, or simly \"all\"")
    @cooldown(8, 60, BucketType.user)
    async def sell_command(self, ctx, animal, amount = "1"):
        if amount.lower() != "all":
            if not amount.isnumeric():
                await ctx.send("that is not a valid amount")
                return
            amount = int(amount)
    
        input = animal.lower()
        await ecoLib.open_account(self, ctx)
        await aniLib.open_zoo(self, ctx)
        
        user = ctx.author

        userNotExist = await aniLib.check_if_zoo_not_exist(user)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        zoo = await aniLib.get_zoo_data()
        data = await aniLib.get_animal_data()
        
        tiers = [
            "common",
            "uncommon",
            "rare",
            "epic",
            "mythical",
        ]
        
        selling = {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "epic": 0,
            "mythical": 0,
        }
        
        if animal not in tiers and animal != "all":
            icon = ""
            for tier in zoo:
                for i in zoo[tier]["animals"]:
                    animal = zoo[tier]["animals"][i]
                    for nick in range(0, len(animal["name"])):
                        if input == animal["name"][nick]:
                            animalName = animal["name"][0]
                            if data[str(user.id)]["animals"][tier][animalName]["count"] == 0:
                                await ctx.send("you don't have that animal")
                                return
                            if amount == "all":
                                selling[tier] += data[str(user.id)]["animals"][tier][animalName]["count"]
                                data[str(user.id)]["animals"][tier][animalName]["count"] = 0
                            
                            else:
                                if data[str(user.id)]["animals"][tier][animalName]["count"] < amount:
                                    await ctx.send("you don't have that many animals")
                                    return
                                selling[tier] += amount
                                data[str(user.id)]["animals"][tier][animalName]["count"] -= amount
                                

                                
                            icon = animal["icon"]
                            break
            
            if icon == "":
                await ctx.send(f"could not find any animal named {input}, sorry")
                return

        
        if animal == "all":
            for tier in zoo:
                for i in zoo[tier]["animals"]:
                    selling[tier] += data[str(user.id)]["animals"][tier][zoo[tier]["animals"][i]["name"][0]]["count"]
                    data[str(user.id)]["animals"][tier][zoo[tier]["animals"][i]["name"][0]]["count"] = 0
                            

        if animal in tiers:
            for tier in zoo:
                if tier == animal:
                    for i in zoo[tier]["animals"]:
                        selling[tier] += data[str(user.id)]["animals"][tier][zoo[tier]["animals"][i]["name"][0]]["count"]
                        data[str(user.id)]["animals"][tier][zoo[tier]["animals"][i]["name"][0]]["count"] = 0
                    break


        tier_prices = {
            "common": 10,
            "uncommon": 50,
            "rare": 150,
            "epic": 600,
            "mythical": 5000,
        }
        
        merchant_colours = [
            0xffb3ba,
            0xffdfba,
            0xffffba,
            0xbaffc9,
            0xbae1ff,
        ]
        
        merchant_emojis = [
            "🧑‍🌾",
            "🧑🏻‍🌾",
            "🧑🏼‍🌾",
            "🧑🏽‍🌾",
            "🧑🏾‍🌾",
            "🧑🏿‍🌾",
        ]
        
        merchant = random.randrange(0, len(merchant_colours))
        merchant_emoji = random.choice(merchant_emojis)
        
        soldstr = ""
        payout = 0
        differentTiersSold = 0
        differentAnimalsSold = 0
        for price, animalAmount in zip(tier_prices.items(), selling.items()):
            if animalAmount[1] != 0:
                soldstr += f"{animalAmount[1]} {price[0]} animal for {price[1]} <:beaverCoin:968588341291397151>"
                if animalAmount[1] >= 2:
                    soldstr += f" each, for a total of {price[1]*animalAmount[1]} <:beaverCoin:968588341291397151>"
                soldstr += "\n"
                
                payout += price[1]*animalAmount[1]
                
                differentTiersSold += 1
                differentAnimalsSold += animalAmount[1]
        
        if floor(payout*(1+merchant*0.01))-payout > random.randint(15, 25):
            soldstr += f"\nSince i'm feeling generous, i gave you an extra {floor(payout*(1+merchant*0.01))-payout} <:beaverCoin:968588341291397151>"
            payout = floor(payout*(1+merchant*0.01))
        
        with open("storage/playerInfo/animals.json", "w") as f:
            json.dump(data, f)
        await ecoLib.update_bank_data(ctx.author, round(payout))
        
        if differentTiersSold != 1:
            soldstr += f"\n\n\nI bought a total of {differentAnimalsSold} animals for {payout} <:beaverCoin:968588341291397151>\nPlease come again!"
            
        
        embed = discord.Embed()
        embed.title = f"{merchant_emoji} Merchant"
        embed.colour = merchant_colours[merchant]
        embed.add_field(name="||\n||", value=soldstr)
        

        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(ecoshop(bot))
