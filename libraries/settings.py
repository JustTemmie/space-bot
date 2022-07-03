import json

async def get_user_settings():
    with open("storage/playerInfo/settings.json", "r") as f:
        settings = json.load(f)
    return settings

async def get_all_settings():
    with open("storage/settings.json", "r") as f:
        settings = json.load(f)
    return settings

async def store_settings(user):
    data = await get_user_settings()
    
    if str(user.id) in data:
        data[str(user.id)]["version"] = 1.00
        with open("storage/playerinfo/settings.json", "w") as f:
            json.dump(data, f)
        
        data = await get_user_settings()
        
        return


    data[str(user.id)] = {}
    data[str(user.id)]["version"] = 1.00
    
    data[str(user.id)]["vote"] = {}
    data[str(user.id)]["vote"]["reminder"] = False
    
    
    with open("storage/playerinfo/settings.json", "w") as f:
        json.dump(data, f)

    return True