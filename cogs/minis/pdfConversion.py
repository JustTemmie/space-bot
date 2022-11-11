import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from pdf2image import convert_from_path
from PIL import Image
import functools
from typing import Optional
import subprocess
import io
import string

class pdfConversion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        name="pdf2image",
        aliases=["pdf2png", "pdf2jpg"],
        brief="converts your pdf into a png",
    )
    @cooldown(1, 5, BucketType.user)
    async def calendar(self, ctx, dpi=450):
        if dpi >= 450 and 725539745572323409 != ctx.author.id:
            await ctx.send("lowering dpi to 450")
            dpi = 450
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            data = await attachment.read()
            filename = attachment.filename
        else:
            return await ctx.send("You forgot the image.")

        async with ctx.typing():
            with open(f"temp/{ctx.author.id}-{filename}.pdf", "wb") as f:
                f.write(data)
            convert_from_path(f"temp/{ctx.author.id}-{filename}.pdf", dpi=dpi)[0].save(f"temp/{ctx.author.id}-{filename}.png", "PNG")

            await ctx.reply(file=discord.File(f"temp/{ctx.author.id}-{filename}.png"))
            
    

async def setup(bot):
    await bot.add_cog(pdfConversion(bot))
