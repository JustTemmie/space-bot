# taken from here https://github.com/philliphqs/hqs.bot/blob/master/hqs.bot-rewrite/cogs/games.py lmao


import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import random


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def minesweeper(self, ctx):
        field00 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field01 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field02 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field03 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field04 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field05 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field06 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field07 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field08 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field10 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field11 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field12 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field13 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field14 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field15 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field16 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field17 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field18 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field20 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field21 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field22 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field23 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field24 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field25 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field26 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field27 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field28 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field30 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field31 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field32 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field33 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field34 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field35 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field36 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field37 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field38 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field40 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field41 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field42 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field43 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field44 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field45 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field46 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field47 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field48 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field50 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field51 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field52 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field53 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field54 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field55 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field56 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field57 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field58 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field60 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field61 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field62 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field63 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field64 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field65 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field66 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field67 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field68 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field70 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field71 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field72 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field73 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field74 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field75 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field76 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field77 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field78 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        field80 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field81 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field82 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field83 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field84 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field85 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field86 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field87 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])
        field88 = random.choice(["1️⃣", "2️⃣", "3️⃣", "💥"])

        minesweeper = f"""
            || {field00} || || {field10} || || {field20} || || {field30} || || {field40} || || {field50} || || {field60} || || {field70} || || {field80} ||
            || {field01} || || {field11} || || {field21} || || {field31} || || {field41} || || {field51} || || {field61} || || {field71} || || {field81} ||
            || {field02} || || {field12} || || {field22} || || {field32} || || {field42} || || {field52} || || {field62} || || {field72} || || {field82} ||
            || {field03} || || {field13} || || {field23} || || {field33} || || {field43} || || {field53} || || {field63} || || {field73} || || {field83} ||
            || {field04} || || {field14} || || {field24} || || {field34} || || {field44} || || {field54} || || {field64} || || {field74} || || {field84} ||
            || {field05} || || {field15} || || {field25} || || {field35} || || {field45} || || {field55} || || {field65} || || {field75} || || {field85} ||
            || {field06} || || {field16} || || {field26} || || {field36} || || {field46} || || {field56} || || {field66} || || {field76} || || {field86} ||
            || {field07} || || {field17} || || {field27} || || {field37} || || {field47} || || {field57} || || {field67} || || {field77} || || {field87} ||
            || {field08} || || {field18} || || {field28} || || {field38} || || {field48} || || {field58} || || {field68} || || {field78} || || {field88} ||
            """
        m = discord.Embed(color=ctx.author.color, description=minesweeper)
        m.set_author(name="Minesweeper")  # , url=botsetup.website, icon_url=links.minesweeper)
        # m.set_footer(text=wm.footer)
        await ctx.send(embed=m)


async def setup(bot):
    await bot.add_cog(test(bot))
