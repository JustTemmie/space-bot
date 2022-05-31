import json


async def open_zoo(user):
    users = await get_animal_data()
    
    if str(user.id) in users:
        return

    users[str(user.id)] = {}
    
    ##########################################
    
    users[str(user.id)]["animals"] = {}
    
    users[str(user.id)]["animals"]["common"] = {}
    
    animals = {
        "common": ["snail", "butterfly", "cricket", "bee", "worm", "beetle"],
        "uncommon": [],
        "rare": [],
        "epic": [],
        "mythical": [],
    }

    
    for i in animals:
        
        users[str(user.id)]["animals"][rarity][i] = {}
        users[str(user.id)]["animals"][rarity][i]["caught"] = 0
        users[str(user.id)]["animals"][rarity][i]["count"] = 0
        users[str(user.id)]["animals"][rarity][i]["sold"] = 0
        users[str(user.id)]["animals"][rarity][i]["sacrificed"] = 0
        users[str(user.id)]["animals"][rarity][i]["xp"] = 0
    
    users[str(user.id)]["animals"]["uncommon"] = {}
    users[str(user.id)]["animals"]["uncommon"]["dog"] = {}
    users[str(user.id)]["animals"]["uncommon"]["cat"] = {}
    users[str(user.id)]["animals"]["uncommon"]["mouse"] = {}
    users[str(user.id)]["animals"]["uncommon"]["pig"] = {}
    users[str(user.id)]["animals"]["uncommon"]["bird"] = {}
    users[str(user.id)]["animals"]["uncommon"]["bat"] = {}
    
    ##########################################
    
    users[str(user.id)]["nicknames"] = {}

    with open("storage/playerInfo/animals.n", "w") as f:
        json.dump(users, f)

    return True
    

async def get_animal_data():
    with open("storage/playerInfo/animals.json", "r") as f:
        users = json.load(f)

    return users
