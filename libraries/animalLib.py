import json

from libraries.miscLib import *
from libraries.economyLib import check_if_not_exist, open_account
from discord import Embed

zoo_version = 1.04

async def check_if_zoo_not_exist(user):
    users = await get_animal_data()

    if str(user.id) in users:
        await update_global_zoo()
        await update_zoo(user)
        
        return False
    
    return True

async def update_zoo(user):
    data = await get_animal_data()
    
    if data[str(user.id)]["version"] < 1.01:
        animals = {
            "common": ["snail", "butterfly", "cricket", "bee", "worm", "beetle"],
            "uncommon": ["dog", "cat", "mouse", "pig", "bird", "bat"],
            "rare": ["duck", "owl", "boar", "fox", "goat", "bear"],
            "epic": ["whale", "dolphin", "seal", "otter", "blowfish", "squid"],
            "mythical": ["scorpion", "monkey", "giraffe", "sheep", "lizard", "snake"],
        }

        for i in animals:
            for nr, x in enumerate(animals[i]):
                data[str(user.id)]["animals"][i][x]["coins"] = 0

        data[str(user.id)]["version"] = 1.01    
        with open("storage/playerInfo/animals.json", "w") as f:
            json.dump(data, f)
        
        data = await get_animal_data()
    
    if data[str(user.id)]["version"] < 1.04:
        
        data[str(user.id)]["team"] = {}
        data[str(user.id)]["team"]["members"] = {}
        
        animal1to6 = [
            "animal1", "animal2", "animal3", "animal4", "animal5", "animal6"
        ]
        
        for animal in animal1to6:
            data[str(user.id)]["team"]["members"][animal] = {}
            data[str(user.id)]["team"]["members"][animal]["name"] = ""
            data[str(user.id)]["team"]["members"][animal]["icon"] = ""
            data[str(user.id)]["team"]["members"][animal]["tier"] = ""
        
        data[str(user.id)]["version"] = 1.04
        with open("storage/playerInfo/animals.json", "w") as f:
            json.dump(data, f)
        
        data = await get_animal_data()
                

async def update_global_zoo():
    return
    data = await get_animal_data()

async def open_zoo(self, ctx):
    user = ctx.author
    data = await get_animal_data()
    
    if str(user.id) in data:
        return
    
    if await check_if_not_exist(ctx.author):
        await open_account(self, ctx)
        
        if await check_if_not_exist(ctx.author):
            return       
    
        

    data[str(user.id)] = {}
    
    ##########################################
    
    data[str(user.id)]["version"] = zoo_version
    
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
            data[str(user.id)]["animals"][i][x]["coins"] = 0
    
    
    ####################################################
    
    data[str(user.id)]["team"] = {}
    data[str(user.id)]["team"]["members"] = {}
        
    animal1to6 = [
        "animal1", "animal2", "animal3", "animal4", "animal5", "animal6"
    ]
    
    for animal in animal1to6:
        data[str(user.id)]["team"]["members"][animal] = {}
        data[str(user.id)]["team"]["members"][animal]["name"] = ""
        data[str(user.id)]["team"]["members"][animal]["icon"] = ""
        data[str(user.id)]["team"]["members"][animal]["tier"] = ""
    
    
    ####################################################

    with open("storage/playerInfo/animals.json", "w") as f:
        json.dump(data, f)

    return True
    

async def open_bot():
    with open("storage/playerInfo/animals.json", "r") as f:
            data = json.load(f)

    data["global"] = {}

    data["global"]["version"] = 1.00

    data["global"]["animals"] = {}
    data["global"]["animals"]["common"] = {}

    animals = {
        "common": ["snail", "butterfly", "cricket", "bee", "worm", "beetle"],
        "uncommon": ["dog", "cat", "mouse", "pig", "bird", "bat"],
        "rare": ["duck", "owl", "boar", "fox", "goat", "bear"],
        "epic": ["whale", "dolphin", "seal", "otter", "blowfish", "squid"],
        "mythical": ["scorpion", "monkey", "giraffe", "sheep", "lizard", "snake"],
    }

    data["global"]["animals"] = {}

    for i in animals:
        data["global"]["animals"][i] = {}

        for nr, x in enumerate(animals[i]):
            data["global"]["animals"][i][x] = {}
            data["global"]["animals"][i][x]["caught"] = 0
            data["global"]["animals"][i][x]["sold"] = 0
            data["global"]["animals"][i][x]["sacrificed"] = 0
            data["global"]["animals"][i][x]["xp"] = 0


    with open("storage/playerInfo/animals.json", "w") as f:
        json.dump(data, f)

async def get_animal_data():
    with open("storage/playerInfo/animals.json", "r") as f:
        data = json.load(f)

    return data