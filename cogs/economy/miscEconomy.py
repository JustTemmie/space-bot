import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType


from libraries.economyLib import *

class ecoeconomy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="vote",
        brief="vote for the bot and get some rewards",
    )
    async def vote_command(self, ctx):
        await ctx.send("vote for the bot on top.gg to earn some rewards!\nhttps://top.gg/bot/765222621779853312/vote")
        
    
    @commands.command(
        name="tutorial",
        aliases=["start", "tut", "economy"],
        brief="tells you the basics of the economy system",
    )
    @cooldown(10, 200, BucketType.user)
    async def tutorial_command(self, ctx, page=1):
        embed = discord.Embed(
            title=f"yeah as if",
            description=f"find it out yourself idiot",
            colour=ctx.author.colour,
        )
        await ctx.send(embed=embed)
        return

        embed = discord.Embed(
            title=f"Tutorial Page: {page}",
            description=f"use `{ctx.prefix}tutorial [page]` to switch pages!",
            colour=ctx.author.colour,
        )
        if page == 1:
            embed.add_field(
                name=f"what is this?",
                value=f"this is the Andromeda economy system, very much based on spaaaaaaaaaaaaaaaaaaaaaaaaaace",
                inline=False,
            )
            embed.add_field(
                name=f"how can i get started?",
                value=f"well, it's simple, just go to the 2nd page of this tutorial and we'll get started",
                inline=False,
            )
            embed.add_field(
                name=f"note",
                value=f"this is still in early access and pretty much everything is subject to change",
                inline=False,
            )

        elif page == 2:
            embed.add_field(
                name=f"The atlas",
                value="here you can find the different categories of commands",
                inline=False,
            )
            embed.add_field(
                name=f"Page 1: Starting help",
                value="tells any newcomers what this is",
                inline=False,
            )
            embed.add_field(
                name=f"Page 2: The atlas",
                value="you are here, this is where you can find the major categories of commands",
                inline=False,
            )
            embed.add_field(
                name=f"Page 3: How to earn money",
                value="this page will tell you most of the ways you can earn some shiny <:beavert:968588341291397151>",
                inline=False,
            )
            # embed.add_field(name = f"Page 4: Upgrades", value = "Upgrades that permanently incrase your production is some sort of way", inline = False)
            # embed.add_field(name = f"Page 5: Gambling", value = "coming soon", inline = False)

        elif page == 3:
            embed.add_field(
                name=f"how to get that cash money",
                value=f"this is the different ways you can persue to get that bank, gamers",
                inline=False,
            )
            embed.add_field(
                name=f"Researching",
                value=f"simply do {ctx.prefix}research, {ctx.prefix}res, or {ctx.prefix}beg - and you'll get free money",
                inline=False,
            )
            embed.add_field(
                name=f"Buying shit",
                value=f"By using {ctx.prefix}shop you can find many different shops you can use, all of which either buff your hourly automatic cash generation, or increases the amount gained from researching",
                inline=False,
            )
            embed.add_field(
                name=f"Gambling :)))",
                value=f"if you don't really care how much money you would like, you can gamble with commands such as {ctx.prefix}slots and you'll get some <:beaverCoin:968588341291397151> every now and again",
                inline=False,
            )

        else:
            embed.add_field(name=f"entity not found", value="try a different page", inline=False)

        embed.set_footer(text=f"page {page} of 3")
        await ctx.send(embed=embed)
    

    @commands.hybrid_command(
        name="leaderboard",
        aliases=["lb", "top"],
        brief="checks the current leaderboard",
    )
    @cooldown(2, 10, BucketType.user)
    async def leaderboard_command(self, ctx, show_top=5):
        await ctx.channel.typing()
        
        users = await get_bank_data()
        if show_top > 10:
            show_top = 10

        leaderboard = []

        for user in users:
            leaderboard.append([user, users[user]["wallet"]])

        leaderboard.sort(key=lambda x: x[1], reverse=True)

        embed = discord.Embed(title=f"Top {show_top} richest people", colour=ctx.author.colour)

        for i in range(0, show_top):
            try:
                user = await self.bot.fetch_user(int(leaderboard[i][0]))
                balance = leaderboard[i][1]
                embed.add_field(
                    name=f"{i+1}. {user.display_name}",
                    value=f"{balance} <:beaverCoin:968588341291397151>",
                    inline=False,
                )
            except Exception as e:
                await ctx.send(f"error: {e}")
                break

        await ctx.reply(embed=embed, mention_author=False)



async def setup(bot):
    await bot.add_cog(ecoeconomy(bot))
