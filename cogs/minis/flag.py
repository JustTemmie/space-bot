
# THIS CODE WAS ORIGINALLY WRITTEN BY THE GITHUB USER @Quantum-Cucumber (found in this repo: https://github.com/Quantum-Cucumber/2magers/blob/master/cogs/images.py)
# it's been slightly modified to fit this bot's library

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from os import listdir
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO

FLAGS = []
for file in listdir("images/flags/"):
    if file.endswith(".png"):
        FLAGS.append(file[:-4])

SEPARATORSLIST = {
    "|": "vertical",
    "-": "horizontal",
    "/": "diagonal /",
    "\\": "diagonal \\",
}

PFP_SIZE = 1024
PFP_BLUR = 40
PFP_BORDER = 50

SEPARATORS = {
    "vertical": ((PFP_SIZE / 2, 0), (PFP_SIZE, 0), (PFP_SIZE, PFP_SIZE), (PFP_SIZE / 2), PFP_SIZE),
    "horizontal": ((0, PFP_SIZE / 2), (PFP_SIZE, PFP_SIZE / 2), (PFP_SIZE, PFP_SIZE), (0, PFP_SIZE)),
    "diagonal /": ((PFP_SIZE, 0), (PFP_SIZE, PFP_SIZE), (0, PFP_SIZE)),
    "diagonal \\": ((0, 0), (PFP_SIZE, 0), (PFP_SIZE, PFP_SIZE)),
}


def circle_crop(image: Image):
    # A transparent layer to place the image onto
    base = Image.new("RGBA", image.size, color=0)
    # Ensure the image is also RGBA
    image = image.convert("RGBA")

    # Create B&W image to be used as the composite mask
    mask_img = Image.new("L", image.size, color=0)
    mask_draw = ImageDraw.Draw(mask_img)
    
    # Create the circular mask in white
    mask_draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)

    # Apply the composite
    return Image.composite(image, base, mask_img)


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "flag",
        aliases = ["pride"],
        brief = "do you want a slighly more pridey pfp?\nfor more info, please initiate the command without any parameters",
    )
    @cooldown(2, 5, BucketType.user)
    async def pride(self, ctx, flag = None, seperator = None, flag_2 = None, blur = "false", user: discord.Member = None):
        
        if flag != None and seperator == None:
            image = Image.open(f"images/flags/{flag.title()}.png")
            output = BytesIO()
            image.save(output, format="png")
            output.seek(0)
            await ctx.send(f"{flag.title()}.png", file=discord.File(output, filename=f"{flag.title()}.png"))
            return
            
        if user == None:
            user = ctx.author
        
        if flag == None:
            embed = discord.Embed()
            embed.title = f"{ctx.prefix}{ctx.command}" + " [flag] [divider] [flag_2] {blur}"
            embed.description = """
Generate a pride flag pfp
Possible values are `progress`, `gay`, `bi`, `lesbian`, `sapphic`, `mlm`, `pan`, `polyamorous`, `polysexual`, `trans`, `agender`, `enby`, `aro`, `ace`, `french`, `genderfluid`, `genderqueer`, `maverique`, `bigender`, `demigender`, `demiboy`, and `demigirl`

You must specify 2 flags, this will put them side-by-side. The divider determines how the flags are split.
Divider can be `-`, `|`, `/`, and `\` - this has to be done even if you only want to use one flag. (just use it twice lol)

`blur` may be set to `true` to blur the background flags

`credit to github user @Quantum-Cucumber for the original code`
"""
            await ctx.send(embed=embed)
            return
        
        if seperator != None:
            if flag_2 == None:
                await ctx.send("You need to specify a second flag in order to use a seperator")
                return
            
            try:
                seperator = SEPARATORSLIST[seperator]
            except:
                await ctx.send("That doesn't seem to be a valid seperator, please try again")
                return
            
            if flag_2.title() not in FLAGS:
                await ctx.send("That second flag doesn't seem to be a valid flag, please try again")
                return

        if flag.title() not in FLAGS:
            await ctx.send("That first flag doesn't seem to be a valid flag, please try again")
            return

        if blur.lower() in ["true", "blur", "1"]:
            blur = True
        else:
            blur = False
        
        
        # Load profile picture as a gif
        asset = user.display_avatar.replace(size=512)
        data = BytesIO(await asset.read())
        # Load the pfp into PIL
        pfp = Image.open(data)
        #pfp = Image.open(BytesIO(pfp))
        # Resize pfp to standardised size, taking into account the border width
        pfp = pfp.resize((PFP_SIZE - PFP_BORDER * 2, PFP_SIZE - PFP_BORDER * 2))
        # Prevent colour mode errors
        pfp = pfp.convert("RGBA")

        # Load and resize the flags
        background = Image.open(f"images/flags/{flag.title()}.png")
        background = background.resize((PFP_SIZE, PFP_SIZE))
        

        if flag_2:
            overlay_flag = Image.open(f"images/flags/{flag_2.title()}.png")
            overlay_flag = overlay_flag.resize((PFP_SIZE, PFP_SIZE))

            # Produce mask
            # Create B&W image to be used as the composite mask
            mask_img = Image.new("L", (PFP_SIZE, PFP_SIZE), color=0)
            mask_draw = ImageDraw.Draw(mask_img)

            # Draw the selected seperator in white onto the mask
            mask_poly = SEPARATORS[seperator]
            mask_draw.polygon(mask_poly, fill=255)

            # Apply the mask
            background = Image.composite(overlay_flag, background, mask_img)

            
        # Apply blur
        if blur:
            background = background.filter(ImageFilter.GaussianBlur(PFP_BLUR))

        # Crop profile picture to a circle
        pfp = circle_crop(pfp)

        # Combine images
        background.paste(pfp, (PFP_BORDER, PFP_BORDER, PFP_SIZE - PFP_BORDER, PFP_SIZE - PFP_BORDER), pfp)

        # Save the byte stream and send in chat
        output = BytesIO()
        background.save(output, format="png")
        output.seek(0)
        await ctx.send(file=discord.File(output, filename="pride.png"))


async def setup(bot):
    await bot.add_cog(Images(bot))
