import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog
import json
import time

from bs4 import BeautifulSoup
import requests

from metno_locationforecast import Place, Forecast
from pdf2image import convert_from_path

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
weather_key = os.getenv("OPENWEATHER")

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
            
        
        with open("data/weatherLocations.json", "r") as f:
            existingLocations = json.load(f)
        
        foundLocally = False
        if input.lower() in existingLocations:
            # + seconds in 2 months, to make sure the coordinates are at least somewhat up to date
            if existingLocations[input.lower()][4] + 5184000 > time.time():
                data = existingLocations[input.lower()] 
                lat = data[0]
                lon = data[1]
                locationName = data[2]
                locationCountry = data[3]
                foundLocally = True
        
        if not foundLocally:
            r = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={input}&limit=1&appid={weather_key}")
            request = json.loads(r.content)
            
            if r.status_code != 200:
                await ctx.send(f"error {request['cod']} occured: {request['message']}")
                return
        
            await ctx.send("downloading coordinates to cache...")
                
            realoutput = request[0]
            lat = realoutput["lat"]
            lon = realoutput["lon"]
            locationName = realoutput["name"]
            locationCountry = realoutput["country"]
            
            existingLocations[input.lower()] = [lat, lon, locationName, locationCountry, time.time()]
            
            with open("data/weatherLocations.json", "w") as f:
                json.dump(existingLocations, f)

        place = Place(input, lat, lon)

        my_forecast = Forecast(
            place,
            "https://github.com/JustTemmie/space-bot, contact me on discord: https://discordapp.com/users/368423564229083137 or snassssssss@gmail.com",
        )
        my_forecast.update()

        forecast = str(my_forecast.data.intervals[0]).split("\n")

        embed = Embed(
            title=f"{forecast[0][:-1]}\nUTC, in {locationName}, {locationCountry}",
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



        with open("data/yrIDs.json", "r") as f:
            yr_places = json.load(f)
        
        # check if we already have the ID stored
        isIDStored = False
        if input.lower() in yr_places:
            # + seconds in 2 months, to make sure the ID up to date in case it ever changes
            if yr_places[input.lower()][1] + 5184000 > time.time():
                ID = yr_places[input.lower()][0]
                isIDStored = True

        if not isIDStored:
            r = requests.get(f"https://www.yr.no/nb/s%C3%B8k?q={input}")
            
            soup = BeautifulSoup(r.content, "html.parser")
            soup = soup.find("ol", class_="search-results-list")
            
            try:
                result = soup.find_all("li")[0]
            except Exception as e:
                await ctx.send(f"Could not find the location in YRs database: {e}")
                return
            
            await ctx.send("downloading yr ID to cache...")
            
            link = result.find("a", class_="search-results-list__item-anchor").get("href")
            ID = link.split("/")[4]
            
            yr_places[input.lower()] = [ID, time.time()]
            
            with open("data/yrIDs.json", "w") as f:
                json.dump(yr_places, f)
            
            
        
        response = requests.get(f"https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/{ID}/")

        with open(f"temp/yr-{ctx.author.id}.pdf", "wb") as f:
            f.write(response.content)

        convert_from_path(f"temp/yr-{ctx.author.id}.pdf", dpi=150)[0].save(f"temp/yr-{ctx.author.id}.png", "PNG")

        av_button = discord.ui.Button(
            label="Open Externally",
            url=f"https://www.yr.no/nb/utskrift/v%C3%A6rvarsel/{ID}/",
            emoji="📩",
        )
        view = discord.ui.View()
        view.add_item(av_button)

        await ctx.send(file=discord.File(f"temp/yr-{ctx.author.id}.png"), view=view)


async def setup(bot):
    await bot.add_cog(weather(bot))
