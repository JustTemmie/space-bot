from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import random
import time

nouns = [
    "beaver"
]


class ball8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="noun", brief="Get a random noun")
    @cooldown(5, 2, BucketType.user)
    async def ball8_command(self, ctx):
        await ctx.edit(random.choice(nouns))


async def setup(bot):
    await bot.add_cog(ball8(bot))
