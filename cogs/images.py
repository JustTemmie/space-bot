import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, when_mentioned_or, command, has_permissions, bot_has_permissions, Greedy, Converter, CheckFailure, Cog



from PIL import Image
from io import BytesIO

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
        data = BytesIO(await asset.read())
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
        data = BytesIO(await asset.read())
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
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((512,100),0)

        pfp.save("images/processed/thicc.png")

        await ctx.send(file = discord.File("images/processed/thicc.png"))



def setup(bot):
    bot.add_cog(images(bot))