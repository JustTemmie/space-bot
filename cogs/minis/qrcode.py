import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import libraries.standardLib as SL 

import qrcode
from PIL import Image

class qrcodegenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "qr",
        brief = "Give it a string and it'll return you a qr code"
    )
    @cooldown(1, 3, BucketType.user)
    async def qrcode(self, ctx, *, input):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(input))
        try:
            qr.make(fit=True)
        except Exception as e:
            return await ctx.send(f"Error: {e}\nThe string is likely too long, sorry about that")
    
        img = qr.make_image(
            fill_color="black",
            back_color="white").convert("RGB")
        
        img.save("temp/qrcode.png")
        await ctx.send(file=discord.File("temp/qrcode.png"))

def setup(bot):
    bot.add_cog(qrcodegenerator(bot))
