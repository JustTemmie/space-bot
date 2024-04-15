from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import random
import time

nouns = [
    "python",
    "goober",
    "creature",
]

for i in range(50):
    nouns.append("beaver")


class stupid_shit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="noun", brief="Get a random noun")
    @cooldown(5, 2, BucketType.user)
    async def noun_command(self, ctx):
        await ctx.send(random.choice(nouns))
    
    @commands.command(name="save", aliases=["sav"])
    @cooldown(5, 2, BucketType.user)
    async def save_command(self, ctx):
        msg = await ctx.reply("saving...")
        time.sleep(2)
        if random.random() > 0.95:
            await msg.reply("error: could not save file")
        else:
            await msg.reply("save file update succesful")


async def setup(bot):
    await bot.add_cog(stupid_shit(bot))
