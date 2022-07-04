import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *
import libraries.standardLib as SL 


class ecomarry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # this code doesn't use any else statements btw 😎 i find it more clean :shrug:
    @commands.command(name="marry", brief = "marry someone! even though, they're probably not even going to be your friend")
    @cooldown(20, 600, BucketType.user)
    @commands.guild_only()
    async def marry_someone(self, ctx, member: discord.Member, ring=None):
        if member == None or member == ctx.author:
            return await ctx.send("please tell me who you want to marry")


        await open_account(self, ctx)
        
        if await check_if_not_exist(ctx.author):
            return await ctx.send("you need to create an account first")
        
        if await check_if_not_exist(member):
            return await ctx.send(f"{await SL.removeat(member.display_name)} does not have an account, they need to create an account first")
        
        data = await get_bank_data()
        
        if data[str(ctx.author.id)]["dam"]["level"] < 1:
            return await ctx.send(f"you need to have a dam to marry someone\nbuild one using {ctx.prefix}!build dam")
        
        if ring == None:
            return await ctx.send(
                f"please tell me what ring you want to use\nCommon\nUncommon\nRare\nEpic\n\nyou can buy rings from the shop using {ctx.prefix}shop 2"
            )
            
        try:
            if data[str(ctx.author.id)]["marriage"][str(member.id)]["ring"] == ring.lower():
                await ctx.send(f"you're already married to {await SL.removeat(member.display_name)} with a {ring} ring")
                return
        except:
            pass

        if ring == "💍":
            return await ctx.send("lmao nice try")
        
        ring_emoji = await get_ring_emoji(ring)
                    
        if ring_emoji == "none":
            return await ctx.send("that's not a valid ring")

        try:
            ring_object = data[str(ctx.author.id)]["inventory"][ring.lower()]
        except:
            return await ctx.send("you don't own that ring")

        try:
            if ring_object <= 0:
                await ctx.send(f"you do not have any rings {ring_emoji} to give {member.mention}")
                return
        except:
            await ctx.send(f"you do not have any rings {ring_emoji} to give {member.mention}")
            return

        await ctx.send(
            f"alright, {ctx.author.mention}, are you sure you want to marry {member.mention}? your ring {ring_emoji} will disentegrate if you do"
        )
        response = await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author, timeout=20
        )
        if response.content.lower() not in confirmations:
            await ctx.send(
                f"apparently {ctx.author.mention} doesn't want to marry {member.mention} afterall"
            )
            return

        if not member.bot:
            await ctx.send(f"alright then, {member.mention}, do you wish to marry {ctx.author.mention}?")
            member_response = await self.bot.wait_for("message", check=lambda m: m.author == member, timeout=20)
            if member_response.content.lower() not in confirmations:
                await ctx.send(f"{member.mention} did not want to marry {ctx.author.mention}, what a shame")
                return

        await ctx.send(
            f"it's a match! {ctx.author.mention} and {member.mention} are now married!! 🥳🥳\nyour marriage will now appear on both of your profiles"
        )

        try:
            timer = data[str(ctx.author.id)]["marriage"][str(member.id)]["time"]
        except:
            timer = time.time()
        
        data = await get_bank_data()
        data[str(ctx.author.id)]["inventory"][ring.lower()] -= 1
        data[str(ctx.author.id)]["marriage"][str(member.id)] = {
            "married": True,
            "married_to": member.id,
            "time": timer,
            "ring": ring.lower(),
        }
        data[str(member.id)]["marriage"][str(ctx.author.id)] = {
            "married": True,
            "married_to": ctx.author.id,
            "time": timer,
            "ring": ring.lower(),
        }

        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)

    @commands.command(name="divorce", brief="divorce your current partner, you fu\*\*\*\*\* hoe")
    @cooldown(15, 600, BucketType.user)
    @commands.guild_only()
    async def divorce_someone(self, ctx, member: discord.Member):
        if member == None or member == ctx.author or member.bot:
            await ctx.send("please tell me who you wish to divorce")
            return

        await open_account(self, ctx)
        
        if await check_if_not_exist(ctx.author):
            return await ctx.send("you need to create an account first")

        if await check_if_not_exist(member):
            return await ctx.send(f"{await SL.removeat(member.display_name)} does not have an account, they need to create an account first")
        
        data = await get_bank_data()

        try:
            data[str(ctx.author.id)]["marriage"][str(member.id)]["married"]
        except:
            await ctx.send(f"you're not married to {await SL.removeat(member.display_name)}")
            return

        await ctx.send(
            f"are you sure you want to divorce {member.mention}?\nyour ring will be disentegrated"
        )
        response = await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author, timeout=20
        )

        if response.content.lower() not in confirmations:
            await ctx.send(
                f"thankfully, {ctx.author.mention} did not want to divorce {member.mention}"
            )
            return

        data[str(ctx.author.id)]["marriage"][str(member.id)] = {
            "married": False,
            "married_to": None,
            "time": 0,
        }
        data[str(member.id)]["marriage"][str(ctx.author.id)] = {
            "married": False,
            "married_to": None,
            "time": 0,
        }
        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"{ctx.author.mention} divorced {member.mention} 💔")


async def setup(bot):
    await bot.add_cog(ecomarry(bot))
