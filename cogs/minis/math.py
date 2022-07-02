from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from math import *

replacement_table = {
    "x": "*",
    "^": "**"
}

class mathCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="math",
        brief="i can do math too!"
    )
    async def math_command(self, ctx, *, equation):
        try:
            for symbol in replacement_table:
                equation = equation.replace(symbol, replacement_table[symbol])
            await ctx.send(f"= {eval(equation)}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(mathCommands(bot))
