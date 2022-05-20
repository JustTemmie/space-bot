from urllib import response
import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *


class ecoinv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="send",
        aliases=["give", "simp", "transfer", "gift"],
        brief="give someone money, you simp :)",
    )
    @cooldown(2, 10, BucketType.user)
    async def send_command(self, ctx, member: discord.Member, amount=None):
        await open_account(ctx.author)
        await open_account(member)

        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to give <:shy:848650912636600320>")
            return

        bal = await update_bank_data(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("you don't have THAT much money, jeezzzz")
            return

        if amount < 0:
            await ctx.send(
                "sorry, you sadly can't give anyone a negative amount of money <:smh:848652740250828821>"
            )
            return

        await update_bank_data(ctx.author, -1 * amount)
        await update_bank_data(member, amount)

        await ctx.send(
            f"{ctx.author.display_name} gave {amount} <:beaverCoin:968588341291397151> to {member.display_name}"
        )
    
    
    @commands.command(
        name="inventory",
        aliases=["inv", "items"],
        brief="lets you check your items n' stuff",
    )
    @cooldown(1, 3, BucketType.user)
    async def inv_command(self, ctx, user: discord.Member = None):

        if user is None:
            user = ctx.author

        n = 0

        await open_account(ctx.author)
        users = await get_bank_data()
        items = await get_items_data()

        try:
            inv = users[str(user.id)]["inventory"]
        except:
            inv = []

        embed = discord.Embed(title=f"{user.display_name}'s Inventory", color=ctx.author.color)

        for item in inv:
            for i in items:
                if item == i and inv[item] >= 1:
                    embed.add_field(
                        name=f"{items[i][0]} {items[i][1]}",
                        value=f"{inv[item]}",
                        inline=False,
                    )
                    n += 1

        if n == 0:
            embed.add_field(
                name="Empty",
                value=f"{user.display_name} does not have any items in their inventory",
                inline=False,
            )

        await ctx.send(embed=embed)
    
    
    @commands.command(
        name="balance",
        aliases=["bank", "bal", "money"],
        brief="check your current balance",
    )
    @cooldown(2, 10, BucketType.user)
    async def check_balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        await open_account(user)

        users = await get_bank_data()

        wallet_amount = users[str(user.id)]["wallet"]

        embed = discord.Embed(title=f"{user.display_name}'s balance", colour=ctx.author.colour)
        embed.add_field(
            name="wallet balance",
            value=f"{wallet_amount} <:beaverCoin:968588341291397151>",
        )
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(ecoinv(bot))
