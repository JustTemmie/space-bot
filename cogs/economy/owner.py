import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *
import libraries.standardLib as SL


class ecoowner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ownergive")
    @commands.is_owner()
    async def ownerGiveCommand(self, ctx, member: Member, amount: int):
        if await check_if_not_exist(member):
            return await ctx.send(f"{await SL.removeat(member.display_name)} doesn't have an account, they need to create one first")

        await update_bank_data(member, amount)

        auth = ctx.author.display_name

        await ctx.send(await SL.removeat(f"{ctx.author.display_name} gave {amount} <:beaverCoin:1019212566095986768> to {member.display_name}"))


async def setup(bot):
    await bot.add_cog(ecoowner(bot))
