from urllib import response
import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *


class ecoevents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        await open_account(ctx.author)

        data = await get_bank_data()

        loaded_time = data[str(ctx.author.id)]["speak_cooldown"]

        if loaded_time < time.time():
            data[str(ctx.author.id)]["speak_cooldown"] = time.time() + 450 + random.randint(0, 150)
            if data[str(ctx.author.id)]["spoke_day"] != (datetime.utcnow() - datetime(1970, 1, 1)).days - 1:
                data[str(ctx.author.id)]["spoke_day"] = (datetime.utcnow() - datetime(1970, 1, 1)).days - 1
                data[str(ctx.author.id)]["spoken_today"] = 0
            
            if data[str(ctx.author.id)]["spoken_today"] >= 28:
                return
            
            data[str(ctx.author.id)]["spoken_today"] += 1
            
            with open("data/bank.json", "w") as f:
                json.dump(data, f)

            await update_bank_data(ctx.author, random.randint(2, 5))
            await update_bank_data(ctx.author, 1, "xp")
            
            #with open(f"data/anti-cheat/users/{ctx.author.id}.json", "a") as f:
            #    json.dump(data, f)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        print(user)

        await open_account(user)

        data = await get_bank_data()

        loaded_time = data[str(user.id)]["speak_cooldown"]

        if loaded_time < time.time():
            data[str(user.id)]["speak_cooldown"] = time.time() + 450 + random.randint(0, 150)
            with open("data/bank.json", "w") as f:
                json.dump(data, f)

            await update_bank_data(user, random.randint(2, 5))
            await update_bank_data(user, 1, "xp")
            
def setup(bot):
    bot.add_cog(ecoevents(bot))
