from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord import Embed

import requests 
from bs4 import BeautifulSoup


class blahaj(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blahaj", aliases=["blåhaj"], brief="BLÅHAJ!!!")
    @cooldown(1, 2, BucketType.user)
    async def blahaj_command(self, ctx):
        url = "https://blahaj.sexy"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find('img', class_='stallman')
        image_link = url + image_tag['src']
        
        embed = Embed(
            title=f"{ctx.prefix.title()}!",
            colour=ctx.author.colour,
        )
        
        embed.set_image(url=image_link)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(blahaj(bot))
