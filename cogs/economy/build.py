import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *


dam_emoji = "<:dam:1019212343760142387>"
lodge_emoji = "<:lodge:1019212491143786527>"

class ecobuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def showOverview(data, ctx):
        logs = data[str(ctx.author.id)]["inventory"]["logs"]
        current_damlevel = data[str(ctx.author.id)]["dam"]["level"]
        current_lodgelevel = data[str(ctx.author.id)]["lodge"]["level"]
        
        embed = discord.Embed(
            title="Buildings",
            description="Please specify what you want to work on",
            color=ctx.author.color )
        embed.set_footer(
            text=f"{ctx.author.name}\nLogs:{logs}",
            icon_url=ctx.author.display_avatar.url )

        embed.add_field(
            name=f"{dam_emoji} `Beaver Dam`: LV {current_damlevel}",
            value=f"`{ctx.prefix}build dam`", inline=False, )
        embed.add_field(
            name=f"{lodge_emoji} `Beaver Lodge`: LV {current_lodgelevel}",
            value=f"`{ctx.prefix}build lodge`", inline=False, )

        await ctx.send(embed=embed)
    
    async def buildGenericBuilding(
        self, data, ctx,
        amount, building_levels,
        ID, display_name, emoji):
        current_level = data[str(ctx.author.id)][ID]["level"]

        # if at max level
        if current_level + 1 >= len(building_levels):
            bar = await progress_bar(25, 25, 25)
            embed = discord.Embed(
                title=f"{emoji} {display_name} LV {current_level}",
                description=f"{bar} || MAX level",
                color=ctx.author.color )

        # if not at max level
        else:
            data[str(ctx.author.id)]["inventory"]["logs"] -= amount
            data[str(ctx.author.id)][ID]["spent"]["logs"] += amount
            
            spent = data[str(ctx.author.id)][ID]["spent"]["logs"]
            price_of_next_level = building_levels[current_level + 1][0]

            # if user has spent enough to upgrade their dam's level
            if spent >= price_of_next_level:
                embed = discord.Embed(
                    title=f"{emoji} {display_name}",
                    description=f"You have upgraded your {display_name} to level {current_level+1}",
                    color=ctx.author.color )

                leftOverLogs = spent - price_of_next_level

                data[str(ctx.author.id)][ID]["spent"]["logs"] = 0
                data[str(ctx.author.id)]["inventory"]["logs"] += leftOverLogs
                data[str(ctx.author.id)][ID]["level"] += 1
                
            else:
                bar = await progress_bar(spent, price_of_next_level, 25)
                embed = discord.Embed(
                    title=f"{emoji} {display_name} LV {current_level}",
                    description=f"{bar} || {spent}/{price_of_next_level} to LV {current_level+1}",
                    color=ctx.author.color )
                
                if amount <= 0:
                    embed.set_footer(text=f"{ctx.author.name}, please specify how many logs you want to spend upgrading your {display_name}", icon_url=ctx.author.display_avatar.url)
            

            with open("storage/playerInfo/bank.json", "w") as f:
                json.dump(data, f)
        
        for i in range(1, len(building_levels)):
            if current_level >= i:
                isUnlocked = "**"
            else:
                isUnlocked = ""
            
            embed.add_field(
                name=f"Level {i}:",
                value=f"{isUnlocked}{building_levels[i][1]}{isUnlocked}",
                inline=False )

        await ctx.send(embed=embed)
    
    
    async def buildDam(self, data, ctx, amount):
        dam_levels = [
            [0, ""],
            [1000, f"╰ unlock the {ctx.prefix}marry command"],
            [4000, f"╰ +25% logs from {ctx.prefix}scavenge"],
            [10000, f"╰ something"],
            [15000, f"╰ double coins from {ctx.prefix}daily"],
            [25000, f"╰ another + 25% logs from {ctx.prefix}scavenge"],
        ]
        
        await ecobuild.buildGenericBuilding(
            self, data, ctx,
            amount, dam_levels,
            "dam", "Dam", dam_emoji )
    
    async def buildLodge(self, data, ctx, amount):
        lodge_levels = [
            [0, ""],
            [5000, f"╰ a 20% chance to get a second animals from {ctx.prefix}hunt"],
            [12000, f"╰ another 30% chance to get a second animal from {ctx.prefix}hunt"],
            [25000, f"╰ guarantee a second animal from {ctx.prefix}hunt"],
            [40000, f"╰ +1 brief sense of accomplishment"],
            [55000, f"╰ +1 long lasting sense of accomplishment"],
            [70000, f"╰ a third animal from {ctx.prefix}hunt"],
            [85000, f"╰ +15% to the animal selling price"],
            [100000, f"╰ increase the chance of non-common animals by 20%"],
        ]
        
        await ecobuild.buildGenericBuilding(
            self, data, ctx,
            amount, lodge_levels,
            "lodge", "Lodge", lodge_emoji )
                

    @commands.command(
        name="build",
        aliases=["construct", "buildings", "upgrade"],
        brief="work your way through the build process on your very own dam",
    )
    @cooldown(8, 15, BucketType.user)
    async def build_command(self, ctx, building="none", amount=0):
        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")


        data = await get_bank_data()
        logs = data[str(ctx.author.id)]["inventory"]["logs"]
        amount = round(amount)
        
        if amount < 0:
            return await ctx.send("you can't build with a negative amount of logs?")
        
        if logs < amount:
            return await ctx.send("you don't have that many logs, sorry")
        
            
        match building.lower():
            case ("none"):
                await ecobuild.showOverview(data, ctx)
            case ("dam" | "wall"):
                await ecobuild.buildDam(self, data, ctx, amount)
            case ("lodge" | "hut"):
                await ecobuild.buildLodge(self, data, ctx, amount)


async def setup(bot):
    await bot.add_cog(ecobuild(bot))
