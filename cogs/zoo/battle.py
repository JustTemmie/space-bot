import discord
from discord.ui import Button, View, Select
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from io import BytesIO
import PIL

import libraries.standardLib as SL
import libraries.animalLib as aniLib
from libraries.economyLib import *
from libraries.textBoxes import *


class zooBattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="battle",
        aliases=["b"],
        brief="fight, fight, fight",
    )
    @cooldown(2, 2, BucketType.user)
    async def battleCommand(self, ctx):
        await aniLib.open_zoo(self, ctx)

        # if user is None:
        user = ctx.author

        userNotExist = await aniLib.check_if_zoo_not_exist(user)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        zoo = await aniLib.get_zoo_data()
        data = await aniLib.get_animal_data()

        team = data[str(user.id)]["team"]["members"]

        teamMembers = []
        for pet in team:
            teamMembers.append(team[pet]["name"])

        #await ctx.send(teamMembers)
        await ctx.send(f'{team["animal1"]["icon"]} {team["animal1"]["name"]}')
        
        embed = Embed()
        embed.set_author(name = f"{ctx.author.display_name} runs into battle!", icon_url = ctx.author.display_avatar.url)
        
        animal1 = ""
        animal2 = ""
        animal3 = ""
        
        embed.add_field(
            inline = True,
            name = f"{await SL.removeat(ctx.author.display_name)}'s team",
            value = f"{animal1}\n{animal2}\n{animal3}"
        )
        
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(zooBattle(bot))
