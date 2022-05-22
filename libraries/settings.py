import json

async def get_settings():
    with open("storage/user/settings.json", "r") as f:
        settings = json.load(f)
    return settings

async def store_user_id(user):
    data = await get_settings()
    
    if str(user.id) in data:
        return
    
    data[str(user.id)] = {}
    
    with open("storage/user/settings.json", "w") as f:
        json.dump(data, f)

    return True