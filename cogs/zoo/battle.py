import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from io import BytesIO
import PIL

import libraries.standardLib as SL 
import libraries.animalLib as aniLib
from libraries.economyLib import *
from libraries.textBoxes import *

class zooBattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "battle",
        aliases = ["b"],
        brief = "fight, fight, fight",
    )
    @cooldown(2, 2, BucketType.user)
    async def battleCommand(self, ctx):
        await aniLib.open_zoo(self, ctx)
        
        #if user is None:
        user = ctx.author

        if await aniLib.check_if_zoo_not_exist(user):
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        
        zoo = await aniLib.get_zoo_data()
        data = await aniLib.get_animal_data()
        
        img = PIL.Image.new('RGBA', (1440, 1100), (0, 0, 0, 0))
        
        #font = PIL.ImageFont.truetype("storage/fonts/pixel.ttf", 24)
        draw = PIL.ImageDraw.Draw(img)
        
        
        pets = [
            "storage/battle_data/images/bee.png",
            "storage/battle_data/images/snail.png",
            "storage/battle_data/images/butterfly.png",
        ]
        
        text_boxes = [
            f"HP",
        ]
        
        while len(text_boxes) < len(pets):
            text_boxes.append("")
        
        j = 0
        for i in range(250, 1070+1, 410):
            pet = PIL.Image.open(pets[j], 'r')
            textbox = PIL.Image.new('RGBA', (pet.width*2, round(pet.height*1.5)), (255, 255, 255, 200))
            
            img.paste(pet, (i, img.height - pet.height - textbox.height - 80))
            img.paste(textbox, (i + round(pet.width / 2) - round(textbox.width / 2), img.height - textbox.height - 50))
            
            xstart:int = i + 5 + round(pet.width / 2) - round(textbox.width / 2)
            ystart:int = img.height - textbox.height - 45
            text_box(
                text_boxes[j],
                draw,
                font("storage/fonts/pixel.ttf", 24),
                (xstart, ystart, textbox.width - 10, textbox.height - 10),
                ALLIGNMENT_LEFT,
                ALLIGNMENT_TOP,
                fill=(0,0,0)
            )
            j += 1

        #background.save('temp/out.png')
        
        output = BytesIO()
        img.save(output, format="png")
        output.seek(0)
        await ctx.send(file=discord.File(output, filename="battle.png"))
                
        
        #img.show()     
        

async def setup(bot):
    await bot.add_cog(zooBattle(bot))
