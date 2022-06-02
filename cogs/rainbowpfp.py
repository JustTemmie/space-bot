import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import io
from PIL import Image, ImageDraw
import glob

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
    @cooldown(1, 15, BucketType.default)
    async def rainpfp(self, ctx, user: discord.Member = None, opacity = 0.5, inputDuration = 5.0):
        if user == None:
            user = ctx.author

        asset = user.avatar_url_as(size=512)
        data = io.BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((256, 256), 0)

        #pfp.save("temp/rainbowpfp.png")
        
        ars, ars, ars, a = pfp.split()
        loopCounter = 0
        devision = 25
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

                #create a mask using RGBA to define an alpha channel to make the overlay transparent

                image = Image.new('RGB',pfp.size,(red,green,blue))
                r, g, b = image.split()
                overlay = Image.merge("RGBA", (r, g, b, a))
                output = Image.blend(pfp, overlay, opacity)
                output.save(f"temp/rainbow{loopCounter}.png")

        await make_gif("temp/rainbow", inputDuration)
        await ctx.send("done!")#file=discord.File(f"temp/rainbow{loopCounter}.png"))
                
                
                

async def make_gif(frame_folder, inputDuration):
    frames = []
    for image in glob.glob(f'{frame_folder}*.png'):
        frames.append(image)
    
    frames.sort
    print(frames)
    frame_one = frames[0]
    frame_one.save("temp/rainbow.gif", format="GIF", append_images=frames,
               save_all=True, duration=inputDuration*1000, loop=0)
    
def setup(bot):
    bot.add_cog(rainbowPFP(bot))
