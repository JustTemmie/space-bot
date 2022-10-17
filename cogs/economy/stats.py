import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType


from libraries.economyLib import *


class ecostats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", brief="check or upgrade your stats")
    @cooldown(4, 20, BucketType.user)
    async def stats_command(self, ctx, stat=None, amount=0):
        data = await get_bank_data()

        if amount == 0:
            embed = discord.Embed(title="stats", description="", color=0x00FF00)
            embed.add_field(
                name="Stats:",
                value=f"""
<:Strength:976244446595285032> Strength: **{data[str(ctx.author.id)]["stats"]["strength"]}**
<:Dexterity:976244452014301224> Dexterity: **{data[str(ctx.author.id)]["stats"]["dexterity"]}**
<:Intelligence:976244476710359171> Intelligence: **{data[str(ctx.author.id)]["stats"]["intelligence"]}**
<:Wisdom:976244483190558761> Wisdom: **{data[str(ctx.author.id)]["stats"]["wisdom"]}**
<:Charisma:976244498738855966> Charisma: **{data[str(ctx.author.id)]["stats"]["charisma"]}**
<:Perception:976244488894816366> Perception: **{data[str(ctx.author.id)]["stats"]["perception"]}**
<:Free:976244503713308742> Free Points: **{data[str(ctx.author.id)]["stats"]["points"]}**
                    """,
                inline=False,
            )
            embed.set_footer(text=f"use {ctx.prefix}stats <stat> <amount> to upgrade your stats")
            await ctx.send(embed=embed)
            return

        await ctx.send("command not implemented yet")


async def setup(bot):
    await bot.add_cog(ecostats(bot))
