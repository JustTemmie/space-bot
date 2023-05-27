import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import os
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
        name="image2pdf",
        aliases=["png2pdf", "jpg2pdf", "imagetopdf"],
        brief="converts your image into a pdf, supported formats? idk",
    )
    @cooldown(1, 5, BucketType.user)
    async def image2pdf(self, ctx):
        if ctx.message.attachments:
            await ctx.send("downloading images...")
            if not os.path.exists(f"temp/{ctx.author.id}"):
                os.makedirs(f"temp/{ctx.author.id}")

            async with ctx.typing():
                for i, attachment in enumerate(ctx.message.attachments):
                    data = await attachment.read()
                    filename = attachment.filename
                    with open(f"temp/{ctx.author.id}/{filename}-{i}.png ", "wb") as f:
                        f.write(data)
        else:
            return await ctx.send("You forgot the image.")

        await ctx.send("converting...")
        async with ctx.typing():
            try:
                images = []
                for i, file in enumerate(os.listdir(f"temp/{ctx.author.id}")):
                    if i == 0:
                        image1 = Image.open(f"temp/{ctx.author.id}/{file}").convert("RGB")
                    else:
                        images.append(Image.open(f"temp/{ctx.author.id}/{file}").convert("RGB"))
                
                image1.save(f"temp/{ctx.author.id}-output.pdf", save_all=True, append_images=images)
            
                await ctx.reply(file=discord.File(f"temp/{ctx.author.id}-output.pdf"))

            except Exception as e:
                await ctx.send(f"an error occured: {e}")
                
            for file in os.listdir(f"temp/{ctx.author.id}"):
                os.remove(f"temp/{ctx.author.id}/{file}")
            os.removedirs(f"temp/{ctx.author.id}")
            os.remove(f"temp/{ctx.author.id}-output.pdf")
            
    @commands.command(
        name="pdf2image",
        aliases=["pdf2png", "pdf2jpg", "pdftoimage"],
        brief="converts your pdf into a png",
    )
    @cooldown(1, 5, BucketType.user)
    async def pdf2image(self, ctx, dpi=400):
        if dpi > 400 and not ctx.is_owner():
            await ctx.send("lowering dpi to 400")
            dpi = 400
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
