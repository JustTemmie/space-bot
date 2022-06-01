import json


async def open_zoo(user):
    data = await get_animal_data()
    
    
    
    if str(user.id) in data:
        return

    data[str(user.id)] = {}
    
    ##########################################
    
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

    #data[str(user.id)]["animals"]["uncommon"] = {}
    

    with open("storage/playerInfo/animals.json", "w") as f:
        json.dump(data, f)

    return True
    

async def get_animal_data():
    with open("storage/playerInfo/animals.json", "r") as f:
        data = json.load(f)

    return data
