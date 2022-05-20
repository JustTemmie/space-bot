from urllib import response
import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import asyncio
import json


from libraries.economyLib import *


class ecogambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="coinflip",
        aliases=["flip", "cf"],
        brief="flip a coin! if you win you double your bet, if you lose you don't",
    )
    @cooldown(1, 2, BucketType.user)
    async def coinflip(self, ctx, amount=None, side: str = "heads"):
        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to waste")
            return

        amount = int(amount)
        if amount > 50000:
            amount = 50000

        if amount < 5:
            await ctx.send("please bet at leaaaast 5 <:beaverCoin:968588341291397151>")
            return

        await open_account(ctx.author)
        bal = await update_bank_data(ctx.author)

        if amount > bal[0]:
            await ctx.send("you don't have THAT much money")
            return

        coinsides = ["Heads", "Tails"]

        result = coinsides[random.randint(0, 1)]
        msg = await ctx.reply("the the coin was tossed into the air and...")
        await asyncio.sleep(1.0)

        bal = await update_bank_data(ctx.author)
        if amount > bal[0]:
            await msg.edit(
                content=f"{msg.content} it... didn't land??!\n{ctx.author.display_name} won {amount} <:beaverCoin:968588341291397151>"
            )
            return

        if result.lower() == side.lower():
            await update_bank_data(ctx.author, amount, "wallet")
            await msg.edit(
                content=f"{msg.content} it landed on {result}!\n{ctx.author.display_name} won {2*amount} <:beaverCoin:968588341291397151>"
            )
            return

        await update_bank_data(ctx.author, -amount, "wallet")
        await msg.edit(
            content=f"{msg.content} it landed on  {result}!\n{ctx.author.display_name} lost {amount} <:beaverCoin:968588341291397151>"
        )

    @commands.command(
        name="slot",
        aliases=["slots"],
        brief="do you ever wish you didn't have any money? well do i have the solution for YOU, introducing - gambling™",
    )
    @cooldown(1, 5, BucketType.user)
    async def slot_machine_command(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to waste")
            return

        bal = await update_bank_data(ctx.author)

        amount = int(amount)
        if amount > 50000:
            amount = 50000

        if amount > bal[0]:
            await ctx.send("you don't have THAT much money")
            return

        if amount < 3:
            await ctx.send("please bet at leaaaast 3 <:beaverCoin:968588341291397151>")
            return

        if amount < 0:
            await ctx.send("sorry, you have to gamble a positive amount of money")
            return

        final = []

        slot1 = "<a:slots:849627985857871912>"
        slot2 = "<a:slots:849627985857871912>"
        slot3 = "<a:slots:849627985857871912>"

        msg = await ctx.send(str(final)[:-2] + (str(slot1)) + (str(slot2)) + (str(slot3)))
        await asyncio.sleep(2)

        slot1 = random.choice(
            [
                "<:Coal:848602311659618315>",
                "<:Redstone:848604340658241576>",
                "<:Iron:848602645207842846>",
                "<:Gold:848602678031548427>",
                "<:Emerald:848602691337060412>",
                "<:Diamond:848602702132019210>",
            ]
        )
        final.append(slot1)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")
        await asyncio.sleep(1.5)

        slot2 = random.choice(
            [
                "<:Coal:848602311659618315>",
                "<:Redstone:848604340658241576>",
                "<:Iron:848602645207842846>",
                "<:Gold:848602678031548427>",
                "<:Emerald:848602691337060412>",
                "<:Diamond:848602702132019210>",
            ]
        )
        final.append(slot2)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")
        await asyncio.sleep(1.5)

        slot3 = random.choice(
            [
                "<:Coal:848602311659618315>",
                "<:Redstone:848604340658241576>",
                "<:Iron:848602645207842846>",
                "<:Gold:848602678031548427>",
                "<:Emerald:848602691337060412>",
                "<:Diamond:848602702132019210>",
            ]
        )
        final.append(slot3)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")

        bal = await update_bank_data(ctx.author)
        if amount > bal[0]:
            await msg.reply("nice try ||beaver||")
            return

        if (
            final[0] == "<:Diamond:848602702132019210>"
            and final[1] == "<:Diamond:848602702132019210>"
            and final[2] == "<:Diamond:848602702132019210>"
        ):
            await update_bank_data(ctx.author, 19 * amount, "wallet")
            await msg.reply(
                f"{ctx.author.display_name} won {20*amount} <:beaverCoin:968588341291397151>"
            )

        elif (
            final[0] == "<:Emerald:848602691337060412>"
            and final[1] == "<:Emerald:848602691337060412>"
            and final[2] == "<:Emerald:848602691337060412>"
        ):
            await update_bank_data(ctx.author, 9 * amount, "wallet")
            await msg.reply(
                f"{ctx.author.display_name} won {10*amount} <:beaverCoin:968588341291397151>"
            )

        elif (
            final[0] == "<:Gold:848602678031548427>"
            and final[1] == "<:Gold:848602678031548427>"
            and final[2] == "<:Gold:848602678031548427>"
        ):
            await update_bank_data(ctx.author, 13 * amount, "wallet")
            await msg.reply(
                f"{ctx.author.display_name} won {14*amount} <:beaverCoin:968588341291397151>"
            )

        elif (
            final[0] == "<:Iron:848602645207842846>"
            and final[1] == "<:Iron:848602645207842846>"
            and final[2] == "<:Iron:848602645207842846>"
        ):
            await update_bank_data(ctx.author, 6 * amount, "wallet")
            await msg.reply(
                f"{ctx.author.display_name} won {7*amount} <:beaverCoin:968588341291397151>"
            )

        elif (
            final[0] == "<:Redstone:848604340658241576>"
            and final[1] == "<:Redstone:848604340658241576>"
            and final[2] == "<:Redstone:848604340658241576>"
        ):
            await update_bank_data(ctx.author, 5 * amount, "wallet")
            await msg.reply(
                f"{ctx.author.display_name} won {6*amount} <:beaverCoin:968588341291397151>"
            )

        elif (
            final[0] == "<:Coal:848602311659618315>"
            and final[1] == "<:Coal:848602311659618315>"
            and final[2] == "<:Coal:848602311659618315>"
        ):
            await update_bank_data(ctx.author, 4 * amount, "wallet")
            await msg.reply(
                f"{ctx.author.display_name} won {5*amount} <:beaverCoin:968588341291397151>"
            )

        elif final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            await update_bank_data(ctx.author, 0.5 * amount, "wallet")
            await msg.reply(
                f"{ctx.author.display_name} won {1.5*amount} <:beaverCoin:968588341291397151>"
            )

        else:
            await update_bank_data(ctx.author, -1 * amount, "wallet")
            await msg.reply(
                f"<:sadcat:849342846582390834> - {ctx.author.display_name} lost {amount} <:beaverCoin:968588341291397151>"
            )

def setup(bot):
    bot.add_cog(ecogambling(bot))
