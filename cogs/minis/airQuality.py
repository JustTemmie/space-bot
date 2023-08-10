import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog
import json
import time

from datetime import date
import requests

import os
from dotenv import load_dotenv

load_dotenv("keys.env")
weather_key = os.getenv("OPENWEATHER")
air_api = os.getenv("AIRVISUAL")

class airquality(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="air",
        brief="hey what's the air quality?\n don't specify country or state, you can try using country code or state abbreviation\nbut that may or may not work",
    )
    @cooldown(5, 60, BucketType.user)
    async def check_air(self, ctx, *, input):
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
            try:
                r = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={input}&limit=1&appid={weather_key}")
            except:
                await ctx.send("whoops, timed out or somthn")
                return
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

        lat = round(lat, 2)
        lon = round(lon, 2)
        
        url = f"https://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={air_api}"
        
        try:
            r = requests.get(url)
        except:
            await ctx.send("whoops, timed out or somthn")
            return
        data = json.loads(r.content)
        
        embed = Embed(
            title=f"the air quality in {locationName}, {locationCountry} - {date.today().strftime('%b %d')}",
            description=f"lat: {round(data['data']['location']['coordinates'][1], 4)}, lon: {round(data['data']['location']['coordinates'][0], 4)}"
        )
        
        aqius = data['data']['current']['pollution']['aqius']
        quality = ""
       
        colours = [
            0x00e400,
            0xffff00,
            0xff7e00,
            0xFF0000,
            0x8f3f97,
            0x7e0023,
        ]
        
        if aqius <= 50:
            embed.colour = colours[0]
            quality = " (Good)"
        elif aqius <= 100:
            embed.colour = colours[1]
            quality = " (Moderate)"
        elif aqius <= 150:
            embed.colour = colours[2]
            quality = " (Unhealthy for Sensitive Groups)"
        elif aqius <= 200:
            embed.colour = colours[3]
            quality = " (Unhealthy)"
        elif aqius <= 300:
            embed.colour = colours[4]
            quality = " (Very Unhealthy)"
        else:
            embed.colour = colours[5]
            quality = " (Hazardous)"
        

        embed.add_field(name="quality today", value=f"{aqius} aqius{quality}")
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(airquality(bot))
