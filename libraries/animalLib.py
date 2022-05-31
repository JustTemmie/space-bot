import json


async def open_zoo(user):
    users = await get_animal_data()
    
    print(users)
    
    if str(user.id) in users:
        return

    users[str(user.id)] = {}
    
    ##########################################
    
    users[str(user.id)]["animals"] = {}
    
    users[str(user.id)]["animals"]["common"] = {}
    
    animals = {
        "common": ["snail", "butterfly", "cricket", "bee", "worm", "beetle"],
        "uncommon": ["dog", "cat", "mouse", "pig", "bird", "bat"],
        "rare": ["duck", "owl", "boar", "fox", "goat", "bear"],
        "epic": ["whale", "dolphin", "seal", "otter", "blowfish", "squid"],
        "mythical": [],
    }

    users[str(user.id)]["animals"] = {}
    
    for i in animals:
        users[str(user.id)]["animals"][i] = {}
        print(i)
        print(users)
        
        for nr, x in enumerate(animals[i]):
            print(animals[i][nr])
            
            users[str(user.id)]["animals"][i][x] = {}
            users[str(user.id)]["animals"][i][x]["caught"] = 0
            users[str(user.id)]["animals"][i][x]["count"] = 0
            users[str(user.id)]["animals"][i][x]["sold"] = 0
            users[str(user.id)]["animals"][i][x]["sacrificed"] = 0
            users[str(user.id)]["animals"][i][x]["xp"] = 0
        
  
    #users[str(user.id)]["animals"]["uncommon"] = {}
    

    with open("storage/playerInfo/animals.n", "w") as f:
        json.dump(users, f)

    return True
    

async def get_animal_data():
    with open("storage/playerInfo/animals.json", "r") as f:
        users = json.load(f)

    return users
