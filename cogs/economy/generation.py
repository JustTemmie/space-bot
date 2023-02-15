from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *
from libraries.captchaLib import *


class ecogeneration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="daily", brief="get your daily beaver coins here!")
    @cooldown(3, 15, BucketType.user)
    async def daily_command(self, ctx):
        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        bank = await get_bank_data()
        daily_info = bank[str(ctx.author.id)]["daily"]

        if daily_info["day"] == (datetime.utcnow() - datetime(1970, 1, 1)).days:
            return await ctx.send("you already got your daily, come back tomorrow")

        streak = ""
        if daily_info["day"] + 2 < (datetime.utcnow() - datetime(1970, 1, 1)).days - 1:
            if bank[str(ctx.author.id)]["inventory"]["insurance"] >= 1:
                await ctx.send(f"you had a streak of {daily_info['streak']}\n\nbut you own {bank[str(ctx.author.id)]['inventory']['insurance']} insurance totems\ndo you wish to spend a totem in order to mentain your streak or do you want to restart from 0?")
                response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=45)

                if response.content.lower() in confirmations:
                    streak += f"**you used a totem, you have a {daily_info['streak']} day streak!**"
                    bank[str(ctx.author.id)]["inventory"]["insurance"] -= 1

                else:
                    streak += f"**you lost your streak of {daily_info['streak']} days :(**"
                    daily_info["streak"] = 1
            else:
                streak += f"**you lost your streak of {daily_info['streak']} days :(**"
                daily_info["streak"] = 1

        else:
            daily_info["streak"] += 1
            streak += f"**{daily_info['streak']} day streak!**"

        payout = round(random.uniform(60, 120) + round(random.uniform(3.5, 6) * daily_info["streak"]))
        if payout >= 500:
            payout = 500
        
        
        
        # skills
        if bank[str(ctx.author.id)]["dam"]["level"] >= 4:
            payout *= 2
            streak += "\n**you got double coins for having a lvl 4+ dam**"


        today = datetime.utcnow()
        
        # 1st of january
        if today.day == 1 and today.month == 1:
            payout *= 3
            payout += 5000
            streak += "\n\nHappy new years!"
            
        # valentines
        if today.day == 14 and today.month == 2:
            payout += 2000
            streak += "\n\nLove you!\nrings are on sale today!"
        
        # pancake day
        if today.day == 25 and today.month == 3:
            random.seed((datetime.utcnow() - datetime(1970, 1, 1)).days)
            payout += random.randint(400, 600)
            random.seed()
            streak += "\n\nwould you look at that, it's the best day of the year\npancake day!"
            
        # math day
        if today.day == 14 and today.month == 3:
            payout += 314
            streak += "\n\nMATH DAY!"
            
        # St. Patrick's Day 
        if today.day == 17 and today.month == 3:
            payout += 314
            streak += "\n\nHappy gay pot of gold Day "
            
        # waffle day
        if today.day == 25 and today.month == 3:
            random.seed((datetime.utcnow() - datetime(1970, 1, 1)).days)
            payout += random.randint(400, 600)
            random.seed()
            streak += "\n\nholyshit guys it's the best day of the year, it's waffle day!"
            
        # international beaver day
        if today.day == 7 and today.month == 4:
            payout *= 1.5
            payout += 1000
            streak += "\n\nHappy international beaver day!"
        
        # minecraft birthday
        if today.day == 17 and today.month == 5:
            payout *= 1.5
            streak += "\n\nHappy Minecraft aniversary!"
        
        # friendship day :blush:
        if today.day == 6 and today.month == 8:
            payout *= 2
            streak += "\n\nHappy international friendship day everyone!"
        
        # halloween
        if today.day == 31 and today.month == 10:
            payout += 5000
            streak += "\n\nHappy hall-owee-n!\nhttps://www.youtube.com/watch?v=PFrPrIxluWk"
        
        # finish independence (i'm not finish btw lol)
        if today.day == 6 and today.month == 12:
            payout += 500
        streak += "\n\nHappy national sno- i mean finish indepencence day!"
        
        # chrimsi
        if today.day == 24 and today.month == 12:
            bank[str(ctx.author.id)]["inventory"]["logs"] += 1000
            bank[str(ctx.author.id)]["statistics"]["total_logs"] += 1000
            payout += 3000
        streak += "\nand 1000 <:log:1019212550782599220>\n\nMerry Christmas, Eve!\nEnjoy these logs!"
        
    
    
        # if the user claimed the daily within 2 hours of midnight, give some extra coins some of the time 
        random.seed((datetime.utcnow() - datetime(1970, 1, 1)).days)
        if random.randint(0, 150) == 2:            
            if today.hour < 2:
                payout += 3
                streak += "\nwow, it just hit midnight and i'm feeling quite generous today, here's a three cent nickle (+3 <:beaverCoin:1019212566095986768>)"
            
        random.seed()


        # henw
        if ctx.author.id == 411536312961597440:
            payout -= 1

        payout = round(payout)


        bank[str(ctx.author.id)]["wallet"] += payout
        daily_info["day"] = (datetime.utcnow() - datetime(1970, 1, 1)).days
        bank[str(ctx.author.id)]["daily"] = daily_info

        bank[str(ctx.author.id)]["statistics"]["total_coins"] += payout

        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(bank, f)


        # 1st of april
        if today.day == 1 and today.month == 4:
            # henwee code
            if ctx.author.id == 411536312961597440:
                payout += 1
            
            payout *= 1000
            
            # more henwee code
            if ctx.author.id == 411536312961597440:
                payout -= 1

        await ctx.send(f"you got +{payout} <:beaverCoin:1019212566095986768>!\n{streak}")

    @commands.hybrid_command(
        name="scavenge",
        aliases=["scav", "find", "loot"],
        brief="go scavenge for some l ö g <:log:1019212550782599220>",
    )
    @cooldown(1, 300, BucketType.user)
    async def scavenge_logs(self, ctx):
        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        if await check_captcha(self, ctx, 0.7):
            return

        data = await get_bank_data()
        strength = 3  # data[str(ctx.author.id)]["stats"]["strength"]
        perception = 3  # data[str(ctx.author.id)]["stats"]["perception"]

        try:
            temporal = time.time() - data[str(ctx.author.id)]["scavenge_cooldown"] - 300
            payout = (strength * 0.0004 + 0.008) * temporal**0.8 + random.randrange(8, 11) + random.uniform(0.3, 0.8) * strength
            if payout >= 20000:
                payout = 20000
        except:
            temporal = time.time() - data[str(ctx.author.id)]["scavenge_cooldown"]
            # await ctx.send("you have to wait 5 minutes before you can do this again")
            payout = (((perception / 4) * strength * 0.0004 + 0.008) * temporal**0.8 + random.randrange(8, 11) + random.uniform(0.3, 0.8) * strength) / 300 * temporal * 0.8

        # skills
        if data[str(ctx.author.id)]["dam"]["level"] >= 2:
            payout *= 1.25

        if data[str(ctx.author.id)]["dam"]["level"] >= 5:
            payout *= 1.25

        payout = round(payout)

        data = await get_bank_data()
        data[str(ctx.author.id)]["inventory"]["logs"] += payout
        data[str(ctx.author.id)]["statistics"]["total_logs"] += payout
        data[str(ctx.author.id)]["scavenge_cooldown"] = time.time()

        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"you scavenged for <:log:1019212550782599220>, and you found {payout} of them!")


async def setup(bot):
    await bot.add_cog(ecogeneration(bot))
