import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from datetime import datetime

class misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.report_out = self.bot.get_channel(916087513372844052)
        pass
        #print("hi there")

    
    @commands.command(name="cogs", aliases=["categories", "cog", "dev", "developer"], brief="these are the different categories you can check using the help command")
    async def show_cogs(self, ctx):
        cog_embed = Embed(
            title="Cogs to call upon", description="these are the \"types\" of files which you can call upon using the {ctx.prefix}help command - or load functions", colour=0xaf62eb, timestamp=datetime.utcnow())

        fields = [("admin", "commands for admins", True),
            ("economy", "all commands related to money", False),
            ("fun", "just random commands i\'ve added, like wikipedia and fact", True),
            ("images", "lets you do stuff with images", False),
            ("info", "commands that give you information about something - currently broken", True),
            ("utility", "utility commands like setting a reminder", False),
            ("other commands", "polls, prefix, and help", False),
            ("cogs - just for the developer", "admin, economy, economyevents (BE CAREFUL), emotes, events, fun, Help, images, info, misc, polls, prefix, reactions, search, slash, social, utility,", False),
            ("location", "this command is located in misc", False)]

        for name, value, inline in fields:
            cog_embed.add_field(name=name, value=value, inline=inline),
            cog_embed.set_author(name="welcome to space"),
            cog_embed.set_footer(text="Sent from my iPhone"),
            cog_embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/765222621779853312/07d33473a5a8b5fa6adf600967f7692e.png?size=2048")

        await ctx.send(embed = cog_embed)
    
    
    @commands.command(name="report", brief="report bugs so they can be fixed :D (hopefully)")
    @cooldown(5, 300, BucketType.user)
    async def report_commands(self, ctx, input):
        await self.bot.report_out.send(f"`{input}`\n\nsubmitted by {ctx.author} - {ctx.author.id}")
        print(f"{input}\n\nsubmitted by {ctx.author} - {ctx.author.id}")
        



def setup(bot):
    bot.add_cog(misc(bot))