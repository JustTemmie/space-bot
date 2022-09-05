import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *


class ecobuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name = "build",
        aliases = ["construct", "buildings", "upgrade"],
        brief = "work your way through the build process on your very own dam"
    )
    @cooldown(8, 15, BucketType.user)
    async def build_command(self, ctx, building = "None", amount = 0):
        if amount < 0:
            return await ctx.send("you can't build a dam with anegative amount of logs")

        bonus_string = ""

        await open_account(self, ctx)
        
        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        data = await get_bank_data()
        logs = data[str(ctx.author.id)]["inventory"]["logs"]
        current_damlevel = data[str(ctx.author.id)]["dam"]["level"]
        current_lodgelevel = data[str(ctx.author.id)]["lodge"]["level"]

        if building == "None":
            embed = discord.Embed(title="Buildings", description="Please specify what you want to build/upgrade", color=ctx.author.color)
            embed.set_footer(text=f"{ctx.author.name}\nLogs:{logs}", icon_url=ctx.author.display_avatar.url)

            embed.add_field(name=f"<:dam:975903060561887352> `Beaver Dam`: LV {current_damlevel}", value=f"`{ctx.prefix}build dam`", inline=False)
            embed.add_field(name=f"<:lodge:975903060608057404> `Beaver Lodge`: LV {current_lodgelevel}", value=f"`{ctx.prefix}build lodge`", inline=False)

            await ctx.send(embed=embed)
            return


        #amount = 0
        
        if amount == 0:
            bonus_string = "\nPlease specify how many logs you want to use in order to upgrade it"

        #await ctx.send(f"no.")

        if building.lower() == "dam":
            if logs < amount:
                return await ctx.send("you don't have that many logs")

            dam_levels = [
                1000,
                4000,
                10000,
                15000,
                25000,
            ]

            level = current_damlevel

            data[str(ctx.author.id)]["inventory"]["logs"] -= amount
            data[str(ctx.author.id)]["dam"]["spent"]["logs"] += amount
            spent = data[str(ctx.author.id)]["dam"]["spent"]["logs"]

            if level == len(dam_levels):
                next_level = spent + 1
                next_level_str = "MAX"
                bar = await progress_bar(25, 25, 25)

            else:
                next_level = dam_levels[level] # sets the next level var to be the price of the next level, and the next level string to be the price of the next level OR "max" if it's the max level
                next_level_str = f"{spent}/{next_level}"
                bar = await progress_bar(spent, next_level, 25)
    
            if spent >= next_level:
                embed = discord.Embed(title=f"Dam", description=f"You have upgraded your dam to level {level+1}", color=ctx.author.color)
                if level != len(dam_levels)-1:
                    embed.add_field(name="Logs needed for next level", value=f"╰ {dam_levels[level+1]} <:log:970325254461329438>", inline=False)
                    
                data[str(ctx.author.id)]["dam"]["level"] += 1
                leftOverLogs = data[str(ctx.author.id)]["dam"]["spent"]["logs"] - next_level
                
                data[str(ctx.author.id)]["dam"]["spent"]["logs"] = 0
                data[str(ctx.author.id)]["inventory"]["logs"] += leftOverLogs
                
                
                
                newlvl = data[str(ctx.author.id)]["dam"]["level"]
                
                if newlvl == 1:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 2:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 3:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 4:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 5:
                    data[str(ctx.author.id)]["stats"]["points"] += 5
                

            else:
                embed = discord.Embed(title=f"<:dam:975903060561887352> Dam LV {level}", description=f"{bar} || {next_level_str} to LV {level+1}", color=ctx.author.color)


            #if bonus_string == "":
            
            level = data[str(ctx.author.id)]["dam"]["level"]
            
            with open("storage/playerInfo/bank.json", "w") as f:
                json.dump(data, f)
            
            lvl1bold = ""
            lvl2bold = ""
            lvl3bold = ""
            lvl4bold = ""
            lvl5bold = ""
            
            if level >= 1: lvl1bold = "**"
            if level >= 2: lvl2bold = "**"
            if level >= 3: lvl3bold = "**"
            if level >= 4: lvl4bold = "**"
            if level >= 5: lvl5bold = "**"

            lvl1 = f"╰ +2 skill points and unlock the {ctx.prefix}marry command"
            lvl2 = f"╰ +2 skill points and + 25% logs from {ctx.prefix}scavenge"
            lvl3 = f"╰ +2 skill points and unlock the Beaver Lodge"
            lvl4 = f"╰ +2 skill points and double coins from {ctx.prefix}daily"
            lvl5 = f"╰ +5 skill points and another + 25% logs from {ctx.prefix}scavenge"
            
            embed.add_field(name="Level 1:", value=f"{lvl1bold}{lvl1}{lvl1bold}", inline=False)
            embed.add_field(name="Level 2:", value=f"{lvl2bold}{lvl2}{lvl2bold}", inline=False)
            embed.add_field(name="Level 3:", value=f"{lvl3bold}{lvl3}{lvl3bold}", inline=False)
            embed.add_field(name="Level 4:", value=f"{lvl4bold}{lvl4}{lvl4bold}", inline=False)
            embed.add_field(name="Level 5:", value=f"{lvl5bold}{lvl5}{lvl5bold}", inline=False)
            
            embed.set_footer(text=f"{ctx.author.name}{bonus_string}", icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)
            return




        if building.lower() == "lodge":
            if current_damlevel < 3:
                return await ctx.send("You need to upgrade your dam to lvl 3 first")
            
            if logs < amount:
                return await ctx.send("you don't have that many logs")

            lodge_levels = [
                5000,
                10000,
                15000,
                25000,
                3500
            ]

            level = current_lodgelevel

            data[str(ctx.author.id)]["inventory"]["logs"] -= amount
            data[str(ctx.author.id)]["lodge"]["spent"]["logs"] += amount
            spent = data[str(ctx.author.id)]["lodge"]["spent"]["logs"]

            if level == len(lodge_levels):
                next_level = spent + 1
                next_level_str = "MAX"
                bar = await progress_bar(25, 25, 25)

            else:
                next_level = lodge_levels[level] # sets the next level var to be the price of the next level, and the next level string to be the price of the next level OR "max" if it's the max level
                next_level_str = f"{spent}/{next_level}"
                bar = await progress_bar(spent, next_level, 25)
    
            if spent >= next_level:
                embed = discord.Embed(title=f"Lodge", description=f"You have upgraded your lodge to level {level+1}", color=ctx.author.color)
                if level != len(lodge_levels)-1:
                    embed.add_field(name="Logs needed for next level", value=f"╰ {lodge_levels[level+1]} <:log:970325254461329438>", inline=False)
                    
                data[str(ctx.author.id)]["lodge"]["level"] += 1
                leftOverLogs = data[str(ctx.author.id)]["lodge"]["spent"]["logs"] - next_level
                
                data[str(ctx.author.id)]["lodge"]["spent"]["logs"] = 0
                data[str(ctx.author.id)]["inventory"]["logs"] += leftOverLogs
                
                 
                newlvl = data[str(ctx.author.id)]["lodge"]["level"]
                
                if newlvl == 1:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 2:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 3:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 4:
                    data[str(ctx.author.id)]["stats"]["points"] += 2
                if newlvl == 5:
                    data[str(ctx.author.id)]["stats"]["points"] += 5
                

            else:
                embed = discord.Embed(title=f"<:lodge:975903060608057404> lodge LV {level}", description=f"{bar} || {next_level_str} to LV {level+1}", color=ctx.author.color)


            #if bonus_string == "":
            
            level = data[str(ctx.author.id)]["lodge"]["level"]
            
            with open("storage/playerInfo/bank.json", "w") as f:
                json.dump(data, f)
            
            lvl1bold = lvl2bold = lvl3bold = lvl4bold = lvl5bold = ""
            
            if level >= 1: lvl1bold = "**"
            if level >= 2: lvl2bold = "**"
            if level >= 3: lvl3bold = "**"
            if level >= 4: lvl4bold = "**"
            if level >= 5: lvl5bold = "**"

            lvl1 = f"╰ +2 skill points and a 20% chance to get a second animals from {ctx.prefix}hunt"
            lvl2 = f"╰ +2 skill points another 30% chance to get a second animal from {ctx.prefix}hunt"
            lvl3 = f"╰ +2 skill points guarantee a second animal from {ctx.prefix}hunt"
            lvl4 = f"╰ +2 skill points and unlock the Beaver Lodge"
            lvl5 = f"╰ +5 skill points and another +18 coolness from {ctx.prefix}hunt"
            
            embed.add_field(name="Level 1:", value=f"{lvl1bold}{lvl1}{lvl1bold}", inline=False)
            embed.add_field(name="Level 2:", value=f"{lvl2bold}{lvl2}{lvl2bold}", inline=False)
            embed.add_field(name="Level 3:", value=f"{lvl3bold}{lvl3}{lvl3bold}", inline=False)
            embed.add_field(name="Level 4:", value=f"{lvl4bold}{lvl4}{lvl4bold}", inline=False)
            embed.add_field(name="Level 5:", value=f"{lvl5bold}{lvl5}{lvl5bold}", inline=False)
            
            embed.set_footer(text=f"{ctx.author.name}{bonus_string}", icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)
            return
            
        
        await ctx.send("that's not a valid building")
        return

async def setup(bot):
    await bot.add_cog(ecobuild(bot))
