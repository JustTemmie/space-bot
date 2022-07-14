import random
import json
from re import A
import time
import asyncio

import discord
from captcha.image import ImageCaptcha
from math import floor



async def generate_user_capcha(user):
    # Create an image instance of the given size
    sizes = []
    for i in range(1, 10):
        sizes.append(random.randint(80, 140))

    image = ImageCaptcha(fonts = ["./storage/fonts/captchaFont.ttf"], font_sizes = sizes, width = 500, height = 300)
    
    possibleLetters = "ABCEFGHJKLMNOPRSTUVWXYZ"

    captchaStr = " "
    for i in range(0, 5):
        captchaStr += random.choice(possibleLetters)
        captchaStr += " " * random.randint(1, 4)

    
    # generate the image of the given text
    data = image.generate(captchaStr)
    #image.create_noise_dots(image, color = (0, 0, 0), width = 1, number = 100)
    print(captchaStr)
    
    # write the image on the given file and save it
    image.write(captchaStr, f"./temp/{user.id}captcha.png")
    return captchaStr


async def check_captcha(self, ctx, increase_by = 1):
    with open("./storage/playerInfo/bank.json", "r") as f:
        data = json.load(f)

    counter = data[str(ctx.author.id)]["anti-cheat"]["counter"]
    last_message = data[str(ctx.author.id)]["anti-cheat"]["last_command"]

    time_since_last_message = time.time() - last_message
    timer = time_since_last_message / 600

    decrease_by = floor(timer**0.65)

    data[str(ctx.author.id)]["anti-cheat"]["counter"] += increase_by - decrease_by
    data[str(ctx.author.id)]["anti-cheat"]["last_command"] = time.time()

    if data[str(ctx.author.id)]["anti-cheat"]["counter"] < 0:
        data[str(ctx.author.id)]["anti-cheat"]["counter"] = 0
    
    with open("./storage/playerInfo/bank.json", "w") as f:
        json.dump(data, f)

    # the random number is just because this code can send multiple captchas at once, which isn't ideal lmao
    if counter < 70:
        return False

    if random.randint(0, 50) != 2:
        return False


    captchaStr = await generate_user_capcha(ctx.author)
    captchaStr = captchaStr.replace(" ", "").lower()
    print(f"generated captcha for {ctx.author.id}")
    await ctx.send("you have to solve this captcha first\nexample aderl, case does not matter, no spaces\nif you need help join our support server <https://discord.gg/8MdVe6NgVy>", file = discord.File(f"./temp/{ctx.author.id}captcha.png"))


    check = await check_captcha_valid(self, ctx, captchaStr)


    with open("./storage/playerInfo/bank.json", "r") as f:
        data = json.load(f)
    
    if check:
        data[str(ctx.author.id)]["anti-cheat"]["counter"] = 0
        
    with open("./storage/playerInfo/bank.json", "w") as f:
        json.dump(data, f)
    
    return not check

        
async def check_captcha_valid(self, ctx, captchaStr, loop = 1):
    if loop > 5:
        with open("./storage/playerInfo/bank.json", "r") as f:
            data = json.load(f)
        
        banNr = data[str(ctx.author.id)]["anti-cheat"]["banned_x_times"]
        
        # 12 hours, 24 hours, 48 hours, so on
        bannedFor = 43200*2**banNr
        
        data[str(ctx.author.id)]["anti-cheat"]["banned_x_times"] = banNr + 1
        data[str(ctx.author.id)]["anti-cheat"]["banned_until"] = time.time() + bannedFor
        
        with open("./storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)
        
        await ctx.send(f"You have been **banned** for {round(bannedFor/60/60)} hours due to suspicious activity. This ban will last until <t:{bannedFor + round(time.time())}>\nIf you think this is a mistake, please contact our support server <https://discord.gg/8MdVe6NgVy>")
        
        return False
    
    try:
        response = await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author, timeout=600
        )
    except asyncio.TimeoutError:
        await ctx.send(f"**Timed out** You took too long to answer the captcha!")
        return False


    if response.content.lower() == captchaStr:
        await ctx.send(f"you solved the captcha!")
        return True


    await ctx.send(f"you failed the captcha!\n**Attempt {loop}/5**") 
    return await check_captcha_valid(self, ctx, captchaStr, loop+1)


async def isUserBanned(user):
    with open("./storage/playerInfo/bank.json", "r") as f:
        data = json.load(f)
    
    if data[str(user.id)]["anti-cheat"]["banned_until"] > time.time():
        return True
    
    return False
    