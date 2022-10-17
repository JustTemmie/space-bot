import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog
import json
import requests

from metno_locationforecast import Place, Forecast
from pdf2image import convert_from_path

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
weather_key = os.getenv("OPENWEATHER")

yr_places = {
    "oslo": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-72837/Noreg/Oslo/Oslo/Oslo",
    "trondheim": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-211102/Norge/Tr%C3%B8ndelag/Trondheim/Trondheim",
    "stavanger": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-15183/Norge/Rogaland/Stavanger/Stavanger",
    "sandnes": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-15452/Norge/Rogaland/Sandnes/Sandnes",
    "bergen": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-92416/Norge/Vestland/Bergen/Bergen",
    "drammen": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-58733/Norge/Viken/Drammen/Drammen",
    "fredrikstad": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-33600/Norge/Viken/Fredrikstad/Fredrikstad",
    "porsgrunn": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-31680/Norge/Vestfold%20og%20Telemark/Porsgrunn/Porsgrunn",
    "kristiansand": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-2376/Norge/Agder/Kristiansand/Kristiansand",
    "moss": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-46556/Norge/Viken/Moss/Moss",
    "tromso": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-305409/Norge/Troms%20og%20Finnmark/Troms%C3%B8/Troms%C3%B8",
    "tromsø": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-305409/Norge/Troms%20og%20Finnmark/Troms%C3%B8/Troms%C3%B8",
    "harstad": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-294022/Norge/Troms%20og%20Finnmark/Harstad/Harstad",
    "molde": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-189277/Norge/M%C3%B8re%20og%20Romsdal/Molde/Molde",
    "horten": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-508394/Norge/Vestfold%20og%20Telemark/Horten/Horten",
    "mo i rana": "https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-260276/Norge/Nordland/Rana/Mo%20i%20Rana",
}


class weather(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="weather",
        aliases=["yr"],
        brief="hey what's the weather?\n don't specify country or state, you can try using country code or state abbreviation\nbut that may or may not work\ncan only display the current hour's forecast\nwind direction is 0° when going north, 90° when going east, and so on",
    )
    @cooldown(5, 60, BucketType.user)
    async def check_weather(self, ctx, *, input=None):
        if input == None:
            if ctx.guild.id != 918787074801401868 and ctx.guild.id != 885113462378876948:
                return await ctx.send("Please specify a location.")
            input = "tromsø"

        r = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={input}&limit=1&appid={weather_key}")
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

        if input.lower() in yr_places:
            response = requests.get(yr_places[input.lower()])

            with open("temp/yr.pdf", "wb") as f:
                f.write(response.content)
            convert_from_path("temp/yr.pdf")[0].save("temp/yr.jpg", "JPEG")

            # yr = Image.open("images/processed/yr.jpg")
            # yr = yr.resize((1653*2, 2339*2))
            # yr.save("images/processed/yr.jpg")
            av_button = discord.ui.Button(
                label="Open Externally",
                url="https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/1-305409/Norge/Troms%20og%20Finnmark/Troms%C3%B8/Troms%C3%B8",
                emoji="📩",
            )
            view = discord.ui.View()
            view.add_item(av_button)

            await ctx.send(file=discord.File("temp/yr.jpg"), view=view)


async def setup(bot):
    await bot.add_cog(weather(bot))
