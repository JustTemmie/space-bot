from ast import alias
import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


class rulesandstuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "rules", aliases=["service", "tos"])
    @cooldown(4, 20, BucketType.user)
    async def show_rules_command(self, ctx):
        embed = Embed(
            title=f"{(self.bot.user.name).title()}'s rules",
            color=ctx.author.color
        )

        embed.add_field(name = "Below are links to Andromeda's TOS, privacy policy, and rules", value = "https://github.com/JustTemmie/space-bot/blob/main/rules-and-stuff/service.md\nhttps://github.com/JustTemmie/space-bot/blob/main/rules-and-stuff/privacy-policy.md\nhttps://github.com/JustTemmie/space-bot/blob/main/rules-and-stuff/rules.md", inline = False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(rulesandstuff(bot))
