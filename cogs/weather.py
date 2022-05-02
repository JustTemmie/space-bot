import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, Greedy, CheckFailure, command, has_permissions, bot_has_permissions
import json

from metno_locationforecast import Place, Forecast
       
        
class weather(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "weather", brief = "hey what's the weather?")
    async def check_weather(self, ctx, *, place = "tromsø"):
        if place != "tromsø":
            return await ctx.send("error")

        place = Place("tromsø", 69.69, 19, 30)

        my_forecast = Forecast(place, "metno-locationforecast/1.0 https://github.com/Rory-Sullivan/metno-locationforecast")

        my_forecast.update()
        await ctx.send(my_forecast)

def setup(bot):
    bot.add_cog(weather(bot))