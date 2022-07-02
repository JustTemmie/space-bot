from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from datetime import datetime

import libraries.standardLib as SL

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.report_out_public = self.bot.get_channel(978695335801147435)
        pass
        # print("hi there")

        
    @commands.command(name="report", brief="report bugs so they can be fixed :D (hopefully)")
    @cooldown(5, 300, BucketType.user)
    async def report_command(self, ctx, *, input):
        embed = Embed(name="Report", colour=0xAF62EB, timestamp=datetime.utcnow())
        embed.set_author(name=f"{ctx.author.username} : {ctx.author.id}", icon_url=ctx.author.avatar_url)
        
        
        embed.add_field(name="Report:", value=input, inline=False)        
        await self.bot.report_out_public.send(embed = embed)
        await ctx.send(embed = embed)
        ctx.add_reaction("✅")
        

    @commands.command(name="pound", brief="pound to kg")
    async def poundtokg(self, ctx, *, input):
        await ctx.send(f"{await SL.removeat(input)} pounds is {float(input) * 0.45359237} kg")

    @commands.command(name="kg", brief="kg to pound")
    async def kgtopound(self, ctx, *, input):
        await ctx.send(f"{await SL.removeat(input)} kg is {float(input) * 2.20462262} pounds")

    @commands.command(name="celsius", brief="celsius to fahrenheit")
    async def celsiustofahrenheit(self, ctx, *, input):
        await ctx.send(f"{await SL.removeat(input)} celsius is {float(input) * 1.8 + 32} fahrenheit")

    @commands.command(name="fahrenheit", brief="fahrenheit to celsius")
    async def fahrenheittocelsius(self, ctx, *, input):
        await ctx.send(f"{await SL.removeat(input)} fahrenheit is {(float(input) - 32)/9*5} celsius")


def setup(bot):
    bot.add_cog(misc(bot))
