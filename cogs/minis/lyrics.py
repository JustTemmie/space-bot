import discord
from discord.ui import Select, View
from discord.ext import commands

import requests
from bs4 import BeautifulSoup


class lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="lyrics",
        description="Find the lyrics for a song!"
    )
    @commands.is_owner()
    async def test(self, ctx, song):
        r = requests.get(f"https://genius.com/search?q={song}")
        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find(id="mini_card-title")[0]
        print(result)


async def setup(bot):
    await bot.add_cog(lyrics(bot))