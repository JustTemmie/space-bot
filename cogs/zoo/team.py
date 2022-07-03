from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import libraries.standardLib as SL 
import libraries.animalLib as aniLib
from libraries.economyLib import *

class zooTeam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "team",
        brief = "see your team and change out your members",
    )
    @cooldown(2, 5, BucketType.user)
    async def teamCommand(self, ctx, command = "none", input = None, position = 0):
        await aniLib.open_zoo(self, ctx)
        
        #if user is None:
        user = ctx.author

        if await aniLib.check_if_zoo_not_exist(ctx.author):
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        with open("storage/animals.json", "r") as f:
            zoo = json.load(f)
        
        data = await aniLib.get_animal_data()
        
        if command.lower() in ["add", "set"]:
            if input is None:
                await ctx.send("you need to specify an animal to add or replace an existing one")
                return
            
            names = []
            for tier in zoo:
                for i in zoo[tier]["animals"]:
                    animal = zoo[tier]["animals"][i]
                    for nick in range(0, len(animal["name"])):
                        if input == animal["name"][nick]:
                            icon = animal["icon"]
                            animalTier = tier
                            for name in animal["name"]:
                                names.append(name)
                            break
            
            if input.lower() != "none":
                if input not in names:
                    return await ctx.send(f"{input} was not found")

            if data[str(user.id)]["animals"][animalTier][names[0]]["caught"] == 0:
                    return await ctx.send(f"{input} was not found")
            
            for i in range(1, 6):
                if data[str(user.id)]["team"]["members"][f"animal{i}"]["name"] == names[0]:
                    await ctx.send(f"{input} is already on your team")
                    return
    

            if position >= 1 and position <= 5:
                data[str(user.id)]["team"]["members"][f"animal{position}"]["name"] = names[0]
                data[str(user.id)]["team"]["members"][f"animal{position}"]["icon"] = icon
                
                with open("storage/playerInfo/animals.json", "w") as f:
                    json.dump(data, f)
    
            
            elif position == 0:           
                for i in range(1, 6):
                    team_member= data[str(user.id)]["team"]['members'][f'animal{i}']['name']
                    if team_member == "None":
                        data[str(user.id)]["team"]["members"][f"animal{i}"]["name"] = names[0]
                        data[str(user.id)]["team"]["members"][f"animal{i}"]["icon"] = icon
                        
                        with open("storage/playerInfo/animals.json", "w") as f:
                            json.dump(data, f)
                        
                        break
                
                    if i == 5:
                        return await ctx.send("Sorry, your team is full please specify a position to replace")

            else:
                await ctx.send("please specify a position to replace, between 1 and 5")

        
        embed = Embed()
        
        end = "s"
        if user.display_name[-1:] == "s":
            end = ""
        embed.title = f"{user.display_name}'{end} team"
        embed.colour = user.colour
        embed.description = f"""
`{ctx.prefix}{ctx.command} do something` does this thing
`{ctx.prefix}{ctx.command} do else` does this other thing
"""

        
        for i in range(0, 3):
            icon = data[str(user.id)]['team']['members'][f'animal{i+1}']['icon']
            name = data[str(user.id)]['team']['members'][f'animal{i+1}']['name']
            if name == "None":
                embed.add_field(name = f"{i+1}", value = f"None", inline = True)
            else:
                embed.add_field(name = f"{i+1}", value = f"{icon} {name}", inline = True)
        
        for i in range(3, 5):
            icon = data[str(user.id)]['team']['members'][f'animal{i+1}']['icon']
            name = data[str(user.id)]['team']['members'][f'animal{i+1}']['name']
            if name == "None":
                embed.add_field(name = f"{i+1} benched", value = f"None", inline = True)
            else:
                embed.add_field(name = f"{i+1} benched", value = f"{icon} {name}", inline = True)

            
        await ctx.send(embed=embed)
        
        

def setup(bot):
    bot.add_cog(zooTeam(bot))
