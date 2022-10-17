import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from typing import Optional


from libraries.economyLib import *
import libraries.standardLib as SL


class ecostatistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="statistics",
        brief="show the statistics about some of the things you've done",
    )
    @cooldown(2, 5, BucketType.user)
    async def statistics(self, ctx, user: Optional[discord.Member]):
        if user is None:
            await open_account(self, ctx)
            user = ctx.author

        if user.bot:
            return await ctx.send("i cannot show statistics for bots")

        userNotExist = await check_if_not_exist(user)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        await ctx.channel.typing()

        bankdata = await get_bank_data()

        embed = Embed(title="Statistics", description="from jul 25th 2022", color=user.color)
        embed.set_thumbnail(url=user.display_avatar.url)

        embed.add_field(
            name="Total <:beaverCoin:1019212566095986768> earned",
            value=f"{bankdata[str(user.id)]['statistics']['total_coins']}",
            inline=False,
        )
        embed.add_field(
            name="Total <:log:1019212550782599220> gathered",
            value=f"{bankdata[str(user.id)]['statistics']['total_logs']}",
            inline=False,
        )
        embed.add_field(
            name="Total <:stick:1005255854892781709> eaten",
            value=f"{bankdata[str(user.id)]['statistics']['total_sticks_eaten']}",
            inline=False,
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ecostatistics(bot))
