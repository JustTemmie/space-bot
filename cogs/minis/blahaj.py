from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord import Embed

import random
import time
from requests import request

class blahaj(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blahaj", brief="BLÅHAJ!!!")
    @cooldown(1, 2, BucketType.user)
    async def blahaj_command(self, ctx):
        async with request("GET", "https://blahaj.sexy", headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]
                
                embed = Embed(
                    title=f"Blahaj!",
                    colour=ctx.author.colour,
                )
                
                embed.set_image(url=image_link)
                await ctx.send(embed=embed)

            else:
                await ctx.send("whoopsie doopsie, something went a stinkers")

async def setup(bot):
    await bot.add_cog(blahaj(bot))
