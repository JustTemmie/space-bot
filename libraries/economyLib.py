from datetime import datetime
import json
import random
import time

from libraries.miscLib import *
from discord import Embed
from libraries.captchaLib import isUserBanned


inv_version = 1.1

confirmations = [
        "consent",
        "yes",
        "yess",
        "yes.",
        "yep",
        "yup",
        "yea",
        "y",
        "oui",
        "si",
        "sure",
        "sure?",
        "ok",
        "okay",
        "okay?",
        "i am",
        "beaver",
        "🦫",
        "🥺",
        "😊",
]



async def progress_bar(current, total, witdh = 20):
    percent = int(witdh * current / total)
    bar = "█" * percent + "░" * (witdh - percent)

    return bar


async def get_ring_emoji(ring):
    ring = ring.lower()
    if ring == "common":
            return "<:commoner_ring:970309052053733396>"
    elif ring == "uncommon":
            return "<:uncommon_ring:970309091249516555>"
    elif ring == "rare":
            return "<:rare_ring:970309099134803978>"
    elif ring == "epic":
            return "<:epic_ring:970309107489849435>"
    elif ring == "mythical":
            return "<:mythical_ring:970309114955702372>"
    elif ring == "legendary":
            return "<:legendary_ring:1009857628651917373>"
    else:
            return "none"


async def get_items_data():
    with open("storage/items.json", "r") as f:
        items = json.load(f)

    return items


async def get_shop_data():

    with open("storage/shop.json", "r") as f:
        shop = json.load(f)

    return shop


async def check_if_not_exist(user):
    users = await get_bank_data()

    if str(user.id) in users:        
        if await isUserBanned(user):
            return "banned"
        
        return False
    
    return True


async def update_accounts():
    users = await get_bank_data()
    
    for user in users:

        try:
            users[str(user)]["inventory"]
        except:
            #if users[str(user)]["version"] < 1.00:
            users[str(user)]["inventory"] = {}
            
            users[str(user)]["quote"] = "I'm not a bot, I'm a human"
            
            users[str(user)]["scavenge_cooldown"] = time.time() - 900
            users[str(user)]["inventory"]["logs"] = 0
            
            users[str(user)]["daily"] = {}
            users[str(user)]["daily"]["day"] = 0
            users[str(user)]["daily"]["streak"] = 0

            ###############################################################################
            
            users[str(user)]["spoke_day"] = (datetime.utcnow() - datetime(1970, 1, 1)).days - 1
            users[str(user)]["spoken_today"] = 0
            
            users[str(user)]["dam"] = {}
            users[str(user)]["dam"]["spent"] = {}
            users[str(user)]["dam"]["spent"]["logs"] = 0
            users[str(user)]["dam"]["level"] = 0
            
            users[str(user)]["lodge"] = {}
            users[str(user)]["lodge"]["spent"] = {}
            users[str(user)]["lodge"]["spent"]["logs"] = 0
            users[str(user)]["lodge"]["level"] = 0

            ###############################################################################
            
            users[str(user)]["inventory"]["insurance"] = 0
            
            users[str(user)]["stats"] = {}
            
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            c = random.randint(1, 5)
            d = random.randint(1, 5)
            e = random.randint(1, 5)
            f = random.randint(1, 5)
            
            users[str(user)]["stats"]["strength"] = a
            users[str(user)]["stats"]["dexterity"] = b
            users[str(user)]["stats"]["intelligence"] = c
            users[str(user)]["stats"]["wisdom"] = d
            users[str(user)]["stats"]["charisma"] = e
            users[str(user)]["stats"]["perception"] = f

            users[str(user)]["stats"]["points"] = 30 - (a + b + c + d + e + f)
                
        try:
            users[str(user)]["data"]
        except: 
        #if users[str(user)]["version"] < 1.01:
            users[str(user)]["data"] = {} 
            
            users[str(user)]["dailyvote"] = {}
            users[str(user)]["dailyvote"]["streak"] = 0
            users[str(user)]["dailyvote"]["last_vote"] = 0
            users[str(user)]["dailyvote"]["total_votes"] = 0
            
                    
            with open("storage/playerInfo/bank.json", "w") as f:
                json.dump(users, f)

            users = await get_bank_data()
            
        if users[str(user)]["version"] <= 1.02:
            users[str(user)]["anti-cheat"] = {}
            users[str(user)]["anti-cheat"]["counter"] = 0
            users[str(user)]["anti-cheat"]["last_command"] = time.time()
        
        if users[str(user)]["version"] <= 1.05:
            users[str(user)]["anti-cheat"]["banned_until"] = 0
            users[str(user)]["anti-cheat"]["banned_x_times"] = 0
        
        if users[str(user)]["version"] <= 1.06:
            users[str(user)]["statistics"] = {}
            users[str(user)]["statistics"]["total_logs"] = 0
        
        if users[str(user)]["version"] <= 1.07:
            users[str(user)]["statistics"]["total_coins"] = 0
        
        if users[str(user)]["version"] <= 1.08:
            users[str(user)]["inventory"]["stick"] = 0
        
        if users[str(user)]["version"] <= 1.09:
            users[str(user)]["statistics"]["total_sticks_eaten"] = 0
        
        if str(user) in users:
            users[str(user)]["version"] = inv_version
            
            with open("storage/playerInfo/bank.json", "w") as f:
                        json.dump(users, f)



async def open_account(self, ctx):
    user = ctx.author
    users = await get_bank_data()
    
    if str(user.id) in users:
        return
    
    embed = Embed(
        title="Do you want to open an account?",
        color=ctx.author.color
    )
    
    embed.add_field(name = "If you do, please respond with \"yes\"\nDoing this means you agree to Andromeda's TOS, privacy policy and the rules", value = "||\n||\n\nhttps://github.com/JustTemmie/space-bot/blob/main/rules-and-stuff/service.md\nhttps://github.com/JustTemmie/space-bot/blob/main/rules-and-stuff/privacy-policy.md\nhttps://github.com/JustTemmie/space-bot/blob/main/rules-and-stuff/rules.md", inline = False)
    
    await ctx.send(embed=embed)
    input = await get_input(self, ctx, 30, "please try again")
    
    if input.content not in confirmations:
        await ctx.send("okay, cancelling")
        return
    
    
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 10.0
    users[str(user.id)]["xp"] = 0
    users[str(user.id)]["quote"] = "I'm not a bot, I'm a human"
    
    ###############################################################################

    users[str(user.id)]["scavenge_cooldown"] = time.time() - 900
    users[str(user.id)]["speak_cooldown"] = time.time() + 300
    
    ###############################################################################
    
    users[str(user.id)]["spoke_day"] = (datetime.utcnow() - datetime(1970, 1, 1)).days - 1
    users[str(user.id)]["spoken_today"] = 0

    ###############################################################################
    
    users[str(user.id)]["marriage"] = {}

    ###############################################################################
    
    users[str(user.id)]["inventory"] = {}
    users[str(user.id)]["inventory"]["logs"] = 0
    users[str(user.id)]["inventory"]["insurance"] = 0
    users[str(user.id)]["inventory"]["stick"] = 0

    ###############################################################################
    
    users[str(user.id)]["daily"] = {}
    users[str(user.id)]["daily"]["day"] = 0
    users[str(user.id)]["daily"]["streak"] = 0
    
    ###############################################################################
    
    users[str(user.id)]["dam"] = {}
    users[str(user.id)]["dam"]["spent"] = {}
    users[str(user.id)]["dam"]["spent"]["logs"] = 0
    users[str(user.id)]["dam"]["level"] = 0
    
    ###############################################################################
    
    users[str(user.id)]["lodge"] = {}
    users[str(user.id)]["lodge"]["spent"] = {}
    users[str(user.id)]["lodge"]["spent"]["logs"] = 0
    users[str(user.id)]["lodge"]["level"] = 0

    ###############################################################################
    
    users[str(user.id)]["stats"] = {}
    
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    c = random.randint(1, 5)
    d = random.randint(1, 5)
    e = random.randint(1, 5)
    f = random.randint(1, 5)
    
    users[str(user.id)]["stats"]["strength"] = a
    users[str(user.id)]["stats"]["dexterity"] = b
    users[str(user.id)]["stats"]["intelligence"] = c
    users[str(user.id)]["stats"]["wisdom"] = d
    users[str(user.id)]["stats"]["charisma"] = e
    users[str(user.id)]["stats"]["perception"] = f

    users[str(user.id)]["stats"]["points"] = 30 - (a + b + c + d + e + f)
    
    ###############################################################################
    
    users[str(user.id)]["version"] = inv_version
    
    users[str(user.id)]["data"] = {} 
    
    users[str(user.id)]["dailyvote"] = {}
    users[str(user.id)]["dailyvote"]["streak"] = 0
    users[str(user.id)]["dailyvote"]["last_vote"] = 0
    users[str(user.id)]["dailyvote"]["total_votes"] = 0
    
    ###############################################################################
    
    users[str(user.id)]["anti-cheat"] = {}
    users[str(user.id)]["anti-cheat"]["counter"] = 0
    users[str(user.id)]["anti-cheat"]["last_command"] = time.time()
    users[str(user.id)]["anti-cheat"]["banned_until"] = 0
    users[str(user.id)]["anti-cheat"]["banned_x_times"] = 0
    

    ###############################################################################
    
    users[str(user.id)]["statistics"] = {}
    users[str(user.id)]["statistics"]["total_logs"] = 0
    users[str(user.id)]["statistics"]["total_coins"] = 0
    users[str(user.id)]["statistics"]["total_sticks_eaten"] = 0



    with open("storage/playerInfo/bank.json", "w") as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open("storage/playerInfo/bank.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank_data(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change
    if change > 0:
        users[str(user.id)]["statistics"]["total_coins"] += change

    with open("storage/playerInfo/bank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)][mode]]
    return bal