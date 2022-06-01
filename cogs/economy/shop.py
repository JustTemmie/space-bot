from urllib import response
import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

from typing import Optional


from libraries.economyLib import *


class ecoshop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shop", aliases=["market"], brief="buy something, wouldya?")
    @cooldown(5, 12, BucketType.user)
    async def shop_command(self, ctx, page=1):
        pages = 2
        if page > pages or page <= 0:
            await ctx.send("that page doesn't exist, sorry")
            return

        await open_account(ctx.author)
        shop = await get_shop_data()

        page_bonus_string = {1: "", 2: "**Rings:**\nUse them to marry someone\n"}[page]

        desc = f"Buy something, wouldya?\n\n{page_bonus_string}\n"
        for i in shop:
            if shop[i][2] == page:
                desc += f"{shop[i][1]} `{i}` {shop[i][4]}| {shop[i][0]} <:beaverCoin:968588341291397151>\n{shop[i][3]}"

        embed = discord.Embed(title="🛍 The Market", description=f"{desc}", colour=ctx.author.colour)
        embed.set_footer(text=f"Use {ctx.prefix}buy <item> to buy something\npage {page}/{pages}")

        await ctx.send(embed=embed)

    @commands.command(name="buy", aliases=["transact"], brief="pay for something, wouldya?")
    @cooldown(5, 15, BucketType.user)
    async def buy_command(self, ctx, item, amount: Optional[int] = 1):
        await open_account(ctx.author)

        shop = await get_shop_data()
        bank = await get_bank_data()
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
        
    
    @commands.command(name="sell", brief="try selling your <:log:970325254461329438> for money")
    @cooldown(8, 60, BucketType.user)
    async def sell_command(self, ctx, amount=0):
        return await ctx.send("this command is currently disabled and is going to be reworked into selling animals rather than logs, logs will *stay* unsellable.")
    
        if amount == 0:
            return await ctx.send("please specify an amount of logs to sell")
        
        if amount < 10:
            return await ctx.send("you can't sell less than 10 logs, it's not worth my time")

        await open_account(ctx.author)
        
        data = await get_bank_data()
        charisma = 5#data[str(ctx.author.id)]["stats"]["charisma"]
        # check if the user has enough logs
        if data[str(ctx.author.id)]["inventory"]["logs"] < amount:
            return await ctx.send("you don't have enough logs to sell")
        
        # get the price of the logs
        lower_price = (0.2 * charisma**0.8 + 1.2) 
        price = (0.2 * charisma**0.8) + (random.uniform(1.2, 1.5)) 
        print(price)
        lower_payout = lower_price * amount
        payout = price * amount
        payout **= 1.01
        
        await ctx.send(f"are you sure you want to sell your logs for {round(lower_payout)} <:beaverCoin:968588341291397151>?")
        member_response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=20)
        if member_response.content.lower() not in confirmations:
            await ctx.send(f"alright then, keep your dumb logs")
            return

        # remove the logs from the user's inventory
        data[str(ctx.author.id)]["inventory"]["logs"] -= amount
        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)
            
        # add the money to the user's balance
        await update_bank_data(ctx.author, round(payout))
        
        await ctx.send(f"thank you for your business! here's your {round(lower_payout)} <:beaverCoin:968588341291397151> plus an extra {round(payout)-round(lower_payout)} <:beaverCoin:968588341291397151> i threw in for good measure :)")


def setup(bot):
    bot.add_cog(ecoshop(bot))
