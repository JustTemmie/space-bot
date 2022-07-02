import json

from libraries.miscLib import *
from libraries.economyLib import confirmations
from discord import Embed

zoo_version = 1.00

async def check_if_zoo_not_exist(user):
    users = await get_animal_data()

    if str(user.id) in users:
        await update_global_zoo()
        await update_zoo(user)
        
        return False
    
    return True

async def update_zoo(user):
    return
    data = await get_animal_data()

async def update_global_zoo():
    return
    data = await get_animal_data()

async def open_zoo(self, ctx):
    user = ctx.author
    data = await get_animal_data()
    
    if str(user.id) in data:
        return

    embed = Embed(
        title="Do you want to open a zoo?",
        color=ctx.author.color
    )
    
    embed.add_field(name = "If you do, please respond with \"yes\"\nDoing this means you agree to Andromeda's TOS and privacy policy\n\nhttps://github.com/JustTemmie/space-bot/blob/main/service.md\nhttps://github.com/JustTemmie/space-bot/blob/main/privacy-policy.md", value = "||\n||", inline = False)
    
    await ctx.send(embed=embed)
    input = await get_input(self, ctx, 30, "please try again")
    
    if input.content not in confirmations:
        await ctx.send("okay, cancelling")
        return
    

    data[str(user.id)] = {}
    
    ##########################################
    
    data[str(user.id)]['version'] = zoo_version
    
    data[str(user.id)]["animals"] = {}
    data[str(user.id)]["animals"]["common"] = {}
    
    animals = {
        "common": ["snail", "butterfly", "cricket", "bee", "worm", "beetle"],
        "uncommon": ["dog", "cat", "mouse", "pig", "bird", "bat"],
        "rare": ["duck", "owl", "boar", "fox", "goat", "bear"],
        "epic": ["whale", "dolphin", "seal", "otter", "blowfish", "squid"],
        "mythical": ["scorpion", "monkey", "giraffe", "sheep", "lizard", "snake"],
    }

    data[str(user.id)]["animals"] = {}
    
    for i in animals:
        data[str(user.id)]["animals"][i] = {}
        
        for nr, x in enumerate(animals[i]):
            
            data[str(user.id)]["animals"][i][x] = {}
            data[str(user.id)]["animals"][i][x]["caught"] = 0
            data[str(user.id)]["animals"][i][x]["count"] = 0
            data[str(user.id)]["animals"][i][x]["sold"] = 0
            data[str(user.id)]["animals"][i][x]["sacrificed"] = 0
            data[str(user.id)]["animals"][i][x]["xp"] = 0
        

    with open("storage/playerInfo/animals.json", "w") as f:
        json.dump(data, f)

    return True
    

async def get_animal_data():
    with open("storage/playerInfo/animals.json", "r") as f:
        data = json.load(f)

    return data