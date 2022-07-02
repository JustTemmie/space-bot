import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import io
from PIL import Image
import glob
import os
import time

colours = [
    0xFF0018, # red
    0xFFA52C, # orange
    0xFFFF41, # yellow
    0x008018, # green
    0x0000F9, # blue
    0x86007D, # purple
]

coloursDict = {
    "red": [0xFF, 0x00, 0x18],
    "orange": [0xFF, 0xA5, 0x2C],
    "yellow": [0xFF, 0xFF, 0x41],
    "green": [0x00, 0x80, 0x18],
    "blue": [0x00, 0x00, 0xF9],
    "purple": [0x86, 0x00, 0x7D],
}

colourStr = [
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
]

class rainbowPFP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rainbowpfp", aliases=["rpfp"])
    @cooldown(1, 30, BucketType.default)
    async def rainpfp(self, ctx, user: discord.Member = None, opacity = 0.5, FrameDuration = 100):
        if user == None:
            user = ctx.author

        asset = user.avatar_url_as(size=256)
        data = io.BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((128, 128), 0)

        #pfp.save("temp/rainbowpfp.png")
        
        ars, ars, ars, a = pfp.split()
        loopCounter = 0
        devision = 20
        for x, colour in enumerate(colourStr):
            for i in range(0, devision):
                thestr = ""
                for rgb in range(0,3):
                    try:
                        differnce = coloursDict[colourStr[x+1]][rgb] - coloursDict[colourStr[x]][rgb]
                    except:
                        differnce = coloursDict[colourStr[0]][rgb] - coloursDict[colourStr[x]][rgb]
                    differnceStep = differnce / devision
                    
                    if rgb == 0:
                        red = round(coloursDict[colour][rgb] + (differnceStep * i))
                    elif rgb == 1:
                        green = round(coloursDict[colour][rgb] + (differnceStep * i))
                    elif rgb == 2:
                        blue = round(coloursDict[colour][rgb] + (differnceStep * i))

                loopCounter += 1
                #time.sleep(0.1)

                #create a mask using RGBA to define an alpha channel to make the overlay transparent

                image = Image.new('RGB',pfp.size,(red,green,blue))
                r, g, b = image.split()
                overlay = Image.merge("RGBA", (r, g, b, a))
                output = Image.blend(pfp, overlay, opacity)

                output.save(f"temp/rainbowPFP/rainbow{loopCounter}.png")

        await make_gif("temp/rainbowPFP/rainbow", FrameDuration)
        await ctx.send("done!\nmight look compressed but that's just 8 bit colour :p", file=discord.File("temp/rainbowPFP/output.gif"))
        time.sleep(3)
        for file in glob.glob("temp/rainbowPFP/*"):
            os.remove(file)
                
                
def sortFunc(file):
    return int(file[23:-4])

async def make_gif(frame_folder, inputDuration):
    frames = []
    for file in glob.glob(f"{frame_folder}*.png"):
        frames.append(file)
    frames.sort(key = sortFunc)
    framesObj = [Image.open(frame) for frame in frames]
    frame_one = framesObj[0]
    frame_one.save("temp/rainbowPFP/output.gif", format="GIF", append_images=framesObj,
               save_all=True, duration=inputDuration, loop=0, transparency=0, optimize=True)
    
def setup(bot):
    bot.add_cog(rainbowPFP(bot))
