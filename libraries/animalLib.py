import json

from libraries.miscLib import *
from libraries.economyLib import check_if_not_exist, open_account
from libraries.captchaLib import isUserBanned
from discord import Embed

zoo_version = 1.07

async def check_if_zoo_not_exist(user):
    users = await get_animal_data()

    if str(user.id) in users:
        await update_global_zoo()
        await update_zoo(user)
        
        if await isUserBanned(user):
            return "banned"

        return False
    
    return True

async def update_zoo(user):
    data = await get_animal_data()
    
    if data[str(user.id)]["version"] < 1.05:
        
        data[str(user.id)]["team"] = {}
        data[str(user.id)]["team"]["members"] = {}
        
        animal1to6 = [
            "animal1", "animal2", "animal3", "animal4", "animal5"
        ]
        
        for animal in animal1to6:
            data[str(user.id)]["team"]["members"][animal] = {}
            data[str(user.id)]["team"]["members"][animal]["name"] = "None"
            data[str(user.id)]["team"]["members"][animal]["icon"] = ""
            data[str(user.id)]["team"]["members"][animal]["tier"] = "None"
        
        data[str(user.id)]["version"] = 1.05
        with open("storage/playerInfo/animals.json", "w") as f:
            json.dump(data, f)
        
        data = await get_animal_data()
    
    if data[str(user.id)]["version"] < 1.06:
        data[str(user.id)]["version"] = 1.06
        
        animals = {
            "common": ["snail", "butterfly", "cricket", "bee", "worm", "beetle"],
            "uncommon": ["dog", "cat", "mouse", "pig", "bird", "bat"],
            "rare": ["duck", "owl", "boar", "fox", "goat", "bear"],
            "epic": ["whale", "dolphin", "seal", "otter", "blowfish", "squid"],
            "mythical": ["scorpion", "monkey", "giraffe", "sheep", "lizard", "snake"],
        }
        
        moves = ["move1", "move2", "move3", "move4", "move5", "move6"]
        activeMoves = ["activeMove1", "activeMove2", "activeMove3"]
        
        for i in animals:
            for nr, x in enumerate(animals[i]):
                data[str(user.id)]["animals"][i][x]["coins"] = 0
                
                data[str(user.id)]["animals"][i][x]["moves"] = {}
                
                for move in moves:
                    data[str(user.id)]["animals"][i][x]["moves"][move] = {}
                    data[str(user.id)]["animals"][i][x]["moves"][move]["name"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["id"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["coinsSpent"] = "None"
                
                for move in activeMoves:
                    data[str(user.id)]["animals"][i][x]["moves"][move] = {}
                    data[str(user.id)]["animals"][i][x]["moves"][move]["name"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["id"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["coinsSpent"] = "None"
        
        with open("storage/playerInfo/animals.json", "w") as f:
            json.dump(data, f)

        
        data = await get_animal_data()
        
    if data[str(user.id)]["version"] < 1.07:
        data[str(user.id)]["version"] = 1.07
    
        data[str(user.id)]["animals"]["legendary"] = {}
        legendaries = ["beaver", "wolf", "penguin", "dragon", "unicorn", "snowman"]
        
        i = "legendary"
        for x in legendaries:
            
            data[str(user.id)]["animals"][i][x] = {}
            data[str(user.id)]["animals"][i][x]["caught"] = 0
            data[str(user.id)]["animals"][i][x]["count"] = 0
            data[str(user.id)]["animals"][i][x]["sold"] = 0
            data[str(user.id)]["animals"][i][x]["sacrificed"] = 0
            data[str(user.id)]["animals"][i][x]["xp"] = 0
            data[str(user.id)]["animals"][i][x]["coins"] = 0
            
        animals = {
            "legendary": ["beaver", "wolf", "penguin", "dragon", "unicorn", "snowman"]
        }
        
        moves = ["move1", "move2", "move3", "move4", "move5", "move6"]
        activeMoves = ["activeMove1", "activeMove2", "activeMove3"]
        
        for i in animals:
            for nr, x in enumerate(animals[i]):
                data[str(user.id)]["animals"][i][x]["coins"] = 0
                
                data[str(user.id)]["animals"][i][x]["moves"] = {}
                
                for move in moves:
                    data[str(user.id)]["animals"][i][x]["moves"][move] = {}
                    data[str(user.id)]["animals"][i][x]["moves"][move]["name"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["id"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["coinsSpent"] = "None"
                
                for move in activeMoves:
                    data[str(user.id)]["animals"][i][x]["moves"][move] = {}
                    data[str(user.id)]["animals"][i][x]["moves"][move]["name"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["id"] = "None"
                    data[str(user.id)]["animals"][i][x]["moves"][move]["coinsSpent"] = "None"
        
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
        
        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")       
    
        

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
        "legendary": ["beaver", "wolf", "penguin", "dragon", "unicorn", "snowman"],
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
    
    moves = ["move1", "move2", "move3", "move4", "move5", "move6"]
    activeMoves = ["activeMove1", "activeMove2", "activeMove3"]
    
    for i in animals:
        for nr, x in enumerate(animals[i]):
            
            data[str(user.id)]["animals"][i][x]["moves"] = {}
            
            for move in moves:
                data[str(user.id)]["animals"][i][x]["moves"][move] = {}
                data[str(user.id)]["animals"][i][x]["moves"][move]["name"] = "None"
                data[str(user.id)]["animals"][i][x]["moves"][move]["id"] = "None"
                data[str(user.id)]["animals"][i][x]["moves"][move]["coinsSpent"] = "None"
            
            for move in activeMoves:
                data[str(user.id)]["animals"][i][x]["moves"][move] = {}
                data[str(user.id)]["animals"][i][x]["moves"][move]["name"] = "None"
                data[str(user.id)]["animals"][i][x]["moves"][move]["id"] = "None"
                data[str(user.id)]["animals"][i][x]["moves"][move]["coinsSpent"] = "None"
    
    ####################################################
    
    data[str(user.id)]["team"] = {}
    data[str(user.id)]["team"]["members"] = {}
        
    animal1to6 = [
        "animal1", "animal2", "animal3", "animal4", "animal5"
    ]
    
    for animal in animal1to6:
        data[str(user.id)]["team"]["members"][animal] = {}
        data[str(user.id)]["team"]["members"][animal]["name"] = "none"
        data[str(user.id)]["team"]["members"][animal]["icon"] = "none"
        data[str(user.id)]["team"]["members"][animal]["tier"] = "none"
    
    
    ####################################################

    with open("storage/playerInfo/animals.json", "w") as f:
        json.dump(data, f)

    return True
    

async def open_bot():
    with open("storage/playerInfo/animals.json", "r") as f:
            data = json.load(f)

    data["global"] = {}

    data["global"]["version"] = 1.01

    data["global"]["animals"] = {}
    data["global"]["animals"]["common"] = {}

    animals = {
        "common": ["snail", "butterfly", "cricket", "bee", "worm", "beetle"],
        "uncommon": ["dog", "cat", "mouse", "pig", "bird", "bat"],
        "rare": ["duck", "owl", "boar", "fox", "goat", "bear"],
        "epic": ["whale", "dolphin", "seal", "otter", "blowfish", "squid"],
        "mythical": ["scorpion", "monkey", "giraffe", "sheep", "lizard", "snake"],
        "legendary": ["beaver", "wolf", "penguin", "dragon", "unicorn", "snowman"],
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

async def update_bot_zoo():
    with open("storage/playerInfo/animals.json", "r") as f:
        data = json.load(f)

    if data["global"]["version"] < 1.01:

        data["global"]["version"] = 1.01

        animals = {
            "legendary": ["beaver", "wolf", "penguin", "dragon", "unicorn", "snowman"],
        }

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

async def get_zoo_data():
    with open("storage/animals.json", "r") as f:
        data = json.load(f)

    return data

async def get_animal_data():
    with open("storage/playerInfo/animals.json", "r") as f:
        data = json.load(f)

    return data