from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from time import time
from datetime import datetime

import libraries.economyLib as EL


class showCooldowns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="calendar",
        aliases=["goals"],
        brief="complete daily goals to earn a small reward",
    )
    @cooldown(2, 5, BucketType.user)
    async def calendar(self, ctx):
        await EL.open_account(self, ctx)

        userNotExist = await EL.check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find your inventory, you need to create an account first")

        data = await EL.get_bank_data()

        voteCD = round(time() - data[str(ctx.author.id)]["dailyvote"]["last_vote"])

        embed = Embed(title="Calendar", color=ctx.author.color)

        # if voteCD > 43200:
        #     embed.add_field(name="Vote", value=f"✅", inline=False)
        # else:
        #     timeLeft = await self.time_conversion(abs(43200-voteCD))
        #     embed.add_field(name="Vote", value=f"{timeLeft}", inline=False)

        daily_info = data[str(ctx.author.id)]["daily"]
        if daily_info["day"] == (datetime.utcnow() - datetime(1970, 1, 1)).days:
            desc = f"<t:{round(await self.time_until_end_of_day() + time())}:R>"
        else:
            desc = "✅"
        embed.add_field(name="Daily", value=desc, inline=False)

        await ctx.send(embed=embed)

    @commands.command(
        name="cooldown",
        aliases=["cooldowns", "cd"],
        brief="show the cooldown for a couple commands",
    )
    @cooldown(2, 5, BucketType.user)
    async def cooldown(self, ctx):
        await EL.open_account(self, ctx)

        userNotExist = await EL.check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find your inventory, you need to create an account first")

        embed = Embed(title="Cooldowns", color=ctx.author.color)

        command = self.bot.get_command("scavenge")
        command_cooldown = await self.get_cooldown(command, ctx)
        if command_cooldown > 0:
            desc = f" <t:{command_cooldown+round(time())}:R>"
        else:
            desc = "✅"
        embed.add_field(name="Scavenge", value=desc, inline=False)

        command = self.bot.get_command("hunt")
        command_cooldown = await self.get_cooldown(command, ctx)
        if command_cooldown > 0:
            desc = f" <t:{command_cooldown+round(time())}:R>"
        else:
            desc = "✅"
        embed.add_field(name="Hunt", value=desc, inline=False)

        command = self.bot.get_command("eat")
        command_cooldown = await self.get_cooldown(command, ctx)
        if command_cooldown > 0:
            desc = f"<t:{command_cooldown+round(time())}:R>"
        else:
            desc = "✅"
        embed.add_field(name="Eat", value=desc, inline=False)

        await ctx.send(embed=embed)

    async def get_cooldown(self, command, ctx):
        return round(command.get_cooldown_retry_after(ctx))

    # https://stackoverflow.com/questions/45986035/seconds-until-end-of-day-in-python
    async def time_until_end_of_day(self):
        dt = datetime.utcnow()
        return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)

    # # unused lmao
    # async def time_conversion(self, sec):
    #     sec_value = sec % (24 * 3600)
    #     hour_value = sec_value // 3600
    #     sec_value %= 3600
    #     min_value = sec_value // 60
    #     sec_value %= 60
    #     returnStr = ""
    #     if hour_value >= 1:
    #         returnStr += f"{hour_value}H "
    #     if min_value >= 1:
    #         returnStr += f"{min_value}M "
    #     if sec_value >= 1:
    #         returnStr += f"{sec_value}S"

    #     if returnStr == "":
    #         returnStr = "✅"

    #     return returnStr


async def setup(bot):
    await bot.add_cog(showCooldowns(bot))
