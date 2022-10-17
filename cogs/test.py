import discord
from discord.ui import Select, View
from discord.ext import commands

class testcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "test",
    )
    @commands.is_owner()
    async def test(self, ctx):
        select = Select(
            placeholder="choose your favorite weather",
            options = [
                discord.SelectOption(
                    label="sunny",
                    emoji="☀",
                    description="it's sunny",
                    default=True
                ),
                discord.SelectOption(
                    label="rainy",
                    emoji="☁",
                    description="it's rainy"
                ),
            ]
        )
        
        async def my_callback(interaction):
            await interaction.response.send_message(f"you chose {select.values}")
        
        select.callback = my_callback
        view = View()
        view.add_item(select)
        
        await ctx.send("hi", view=view)
        # https://www.youtube.com/watch?v=56XoybDajjA
    
        

async def setup(bot):
    await bot.add_cog(testcog(bot))
