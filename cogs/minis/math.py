from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from math import *
from interruptingcow import timeout

replacement_table = {
    "x": "*",
    "^": "**"
}

allowedCharacters = "1234567890/*-+()!. "

class mathCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="math",
        brief="i can do math too!"
    )
    @cooldown(120, 1800, BucketType.user)
    async def math_command(self, ctx, *, equation):
        for symbol in replacement_table:
            mathEquation = equation.replace(symbol, replacement_table[symbol])
        try:
            with timeout(5, exception=RuntimeError):
                if set(mathEquation).difference(set(allowedCharacters)):
                    return await ctx.send(f"invalid characters used, please only use the following symbols: `{allowedCharacters}`")
                
                await ctx.send(f"{equation }= {eval(mathEquation)}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(mathCommands(bot))
