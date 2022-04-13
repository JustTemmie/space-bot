import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, when_mentioned_or, command, has_permissions, bot_has_permissions, Greedy, Converter, CheckFailure, Cog

import ascii
import functools
from typing import Optional
import subprocess
import io
import string

from PIL import Image

class images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wanted", aliases=['dead or alive'], brief="do **YOU** want to get someone killed???? well boi do i have the solution")
    @cooldown(2, 5, BucketType.user)
    async def wanted_command(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        
        wanted = Image.open("images/presets/wanted.png")

        asset = user.avatar_url_as(size = 256)
        data = io.BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((227,227))

        wanted.paste(pfp, (150,260))

        wanted.save("images/processed/wanted.png")

        await ctx.send(file = discord.File("images/processed/wanted.png"))

    @commands.command(name="squish", brief="haha person go *squish*")
    @cooldown(2, 5, BucketType.user)
    async def squish_command(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        asset = user.avatar_url_as(size = 512)
        data = io.BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((512,300),0)

        pfp.save("images/processed/thicc.png")

        await ctx.send(file = discord.File("images/processed/thicc.png"))

    @commands.command(name="squishy", brief="haha person go even more squish :)")
    @cooldown(2, 5, BucketType.user)
    async def squishy_command(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        asset = user.avatar_url_as(size = 512)
        data = io.BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((512,100),0)

        pfp.save("images/processed/thicc.png")

        await ctx.send(file = discord.File("images/processed/thicc.png"))

    
    @commands.command(name="ascii", invoke_without_command=True, brief=f"convert image to ascii art\n\nNote how True, False, and None are all case sensitive\nusage: a!ascii (output to text file True or False) (swap black and white True of False) (url for the image, None if you're uploading directly) (what font you want, default is Inconsolata) (a list of all the allowed characters)")
    async def _ascii(self, ctx, out_text: Optional[bool] = False, invert: Optional[bool] = False, url=None, font="Inconsolata", *, charset=string.ascii_letters + string.punctuation + string.digits + " "):
        font = ascii.get_font(font)
        if not font:
            await ctx.send("Invalid font.")
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            data = await attachment.read()
            filename = attachment.filename
        elif url:
            async with self.bot.session.get(url) as resp:
                data = await resp.read()
            filename = url.split("?", 1)[0].rsplit("/", 1)[1]
        else:
            return await ctx.send("You forgot the image.")

        image = Image.open(io.BytesIO(data))
        image = await resize(image, 128)
        
        in_scale = out_scale = 1
        dither = True

        await ctx.send("Performing conversion...")
        result = await self.bot.loop.run_in_executor(None, functools.partial(
            ascii.full_convert,
            image,
            invert=invert,
            font=font,
            spacing=0,
            charset=charset,
            out_text=out_text,
            dither=dither,
            in_scale=in_scale,
            out_scale=out_scale
        ))

        if out_text:
            await ctx.send(file=discord.File(io.BytesIO(result.encode()), filename + ".txt"))
        else:
            out_image = io.BytesIO()
            result.save(out_image, format="png")
            out_image.seek(0)
            if not filename.endswith(".png"):
                filename = "output.png"
            await ctx.send(file=discord.File(out_image, filename))



async def fonts(ctx):
    out = subprocess.check_output(["fc-list", ":mono"]).decode()
    font = set()
    for ln in out.splitlines():
        font.add(ln.split(":")[1].strip())
    await ctx.send(embed=discord.Embed(description="\n".join(font)))

async def resize(image, new_width):
        width, height = image.size
        if width > new_width:
            ratio = new_width / width
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
        return image


def setup(bot):
    bot.add_cog(images(bot))