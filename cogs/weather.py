import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import (
    cooldown,
    BucketType,
    Cog,
    Greedy,
    CheckFailure,
    command,
    has_permissions,
    bot_has_permissions,
)
import json
import requests

from metno_locationforecast import Place, Forecast

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
weather_key = os.getenv("OPENWEATHER")


class weather(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="weather",
        brief="hey what's the weather?\n don't specify country or state, you can try using country code or state abbreviation\nbut that may or may not work\ncan only display the current hour's forecast\nwind direction is 0° when going north, 90° when going east, and so on",
    )
    @cooldown(5, 60, BucketType.user)
    async def check_weather(self, ctx, *, input=None):
        if input == None:
            if ctx.guild.id != 918787074801401868 and ctx.guild.id != 885113462378876948:
                return await ctx.send("Please specify a location.")
            input = "tromsø"
            await ctx.send(
                "read this for more in depth info\n<https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/1-305409/Norge/Troms%20og%20Finnmark/Troms%C3%B8/Troms%C3%B8>"
            )

        r = requests.get(
            f"https://api.openweathermap.org/geo/1.0/direct?q={input}&limit=1&appid={weather_key}"
        )
        request = json.loads(r.content)
        realoutput = request[0]
        lat = realoutput["lat"]
        lon = realoutput["lon"]

        place = Place(input, lat, lon)

        my_forecast = Forecast(
            place,
            "https://github.com/JustTemmie/space-bot, contact me on discord: https://discordapp.com/users/368423564229083137 or snassssssss@gmail.com",
        )
        my_forecast.update()

        forecast = str(my_forecast.data.intervals[0]).split("\n")

        embed = Embed(
            title=f"{forecast[0][:-1]}\nUTC, in {realoutput['name']}, {realoutput['country']}",
            description="",
            color=0x00FF00,
        )

        for a in forecast:
            x = a.split()
            if x[0] != "Forecast":
                if x[0] == "air_temperature:":
                    farenheit = round(float(x[1][:-7]) * 1.8 + 32, 1)
                    embed.add_field(
                        name="air temperature",
                        value=f"{x[1][:-7]}°C, {float(farenheit)}°F",
                        inline=True,
                    )
                else:
                    embed.add_field(name=x[0].replace("_", " "), value=x[1], inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(weather(bot))
