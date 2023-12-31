from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

from datetime import timedelta
import time

from libraries.economyLib import *
from libraries.captchaLib import *
from libraries.standardLib import removeat

gracePeriod = 5
        
class ecogeneration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_red_panda_day(self, year):
        # Start with the first day of September in the given year
        date = datetime(year, 9, 1)

        # Find the first Sunday in September
        while date.weekday() != 6:  # Sunday has weekday index 6 (0 is Monday)
            date += timedelta(days=1)

        # Move to the third Sunday (add 14 days twice)
        date += timedelta(weeks=2)

        return [date.day, date.month]

    def get_easter(self, year):
        y = year
        g = y % 19
        e = 0

        c = y//100
        h = (c - c//4 - (8*c + 13)//25 + 19*g + 15) % 30
        i = h - (h//28)*(1 - (h//28)*(29//(h + 1))*((21 - g)//11))
        j = (y + y//4 + i + 2 - c + c//4) % 7

        # p can be from -6 to 56 corresponding to dates 22 March to 23 May
        # (later dates apply to method 2, although 23 May never actually occurs)
        p = i - j + e
        d = 1 + (p + 27 + (p + 6)//40) % 31
        m = 3 + (p + 26)//30
        return [d, m]
    

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
        if daily_info["day"] + gracePeriod < (datetime.utcnow() - datetime(1970, 1, 1)).days - 1:
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
        
        # make sure these couple events only trigger if the player has an ongoing streak        
        if daily_info["streak"] > 1:
            # award the daily 
            payout += 2 * (daily_info["streak"] // 365)
            
            if daily_info["streak"] % 365 == 0:
                msg1 = await ctx.send(f"**you lost your streak of {daily_info['streak'] - 1} days :(**")
                # i am *evil*
                time.sleep(random.choice[2, 3.2, 4.5, 18])
                await msg1.reply("nah jk bro")
                payout += 10000
                streak += "\n\nyay streak!!!!\n+10000 coins :)\n\nadditionally all future dailies will reward 2 extra coins"
                
            
            if daily_info["streak"] % 50 == 0:
                streak += "omggggg... round streak number 🥺"
                payout + 100
            
        
        # skills
        if bank[str(ctx.author.id)]["dam"]["level"] >= 4:
            payout *= 2
            streak += "\n**you got double coins for having a lvl 4+ dam**"


        today = datetime.utcnow() - timedelta(hours=1)
        
        easterDate = self.get_easter(today.year)
        redpandaDate = self.get_red_panda_day(today.year)
        
        pancakeOffset = timedelta(days = 47)
        pancakeDay = datetime(today.year, easterDate[1], easterDate[0]) - pancakeOffset
        
        # easter
        if today.day == easterDate[0] and today.month == easterDate[1]:
            payout *= 2.5
            payout = round(payout)
            streak += "\n\nHappy Easter!"
        
        # red panda, 3rd sunday of september
        if today.day == redpandaDate[0] and today.month == redpandaDate[1]:
            payout += random.randint(300, 800)
            payout = round(payout)
            streak += "\n\nom g.. it is red panda day:))\ni like those thingies, they cute!!"
        
        if today.day == pancakeDay.day and today.month == pancakeDay.month:
            random.seed((datetime.utcnow() - datetime(1970, 1, 1)).days)
            payout += random.randint(400, 600)
            random.seed()
            streak += "\n\nwould you look at that, it's the best day of the year\npancake day!"

        # 1st of january
        if today.day == 1 and today.month == 1:
            payout *= 3
            payout += 4000
            streak += "\n\nHappy new years!"
        
        # beaver clicker release day
        if today.day == 7 and today.month == 2:
            payout *= 2
            payout += 15
            streak += "\n\nBeaver Clicker Anniversary!"

        # valentines
        if today.day == 14 and today.month == 2:
            payout += 2000
            streak += "\n\nLove you!\nrings are on sale today!"
        
        # math day
        if today.day == 14 and today.month == 3:
            payout += 314
            streak += "\n\nMATH DAY!"
            
        # St. Patrick's Day 
        if today.day == 17 and today.month == 3:
            payout += random.randint(500, 700)
            streak += "\n\nHappy gay pot of gold Day "
            
        # waffle day
        if today.day == 25 and today.month == 3:
            random.seed((datetime.utcnow() - datetime(1970, 1, 1)).days)
            payout += random.randint(400, 600)
            random.seed()
            streak += "\n\nholyshit guys it's the best day of the year, it's waffle day!"
            
        # international beaver day
        if today.day == 7 and today.month == 4:
            bank[str(ctx.author.id)]["inventory"]["logs"] += 2500
            bank[str(ctx.author.id)]["statistics"]["total_logs"] += 2500
            payout *= 1.5
            payout += 1000
            streak += "\n\nHappy international beaver day!\nThe beavers just so happen to have collected 2500 <:log:1019212550782599220> for you!"
        
        # minecraft birthday
        if today.day == 17 and today.month == 5:
            payout *= 1.5
            streak += "\n\nHappy Minecraft aniversary!"
        
        # ice cream day
        if today.day == 1 and today.month == 7:
            payout += 500
            streak += "\n\noh wow, would you look at that\nit's the national creative ice cream flavours day!\n\n(go get yourself some ice cream with funky flavours)"
        
        # belerussian independence day
        if today.day == 3 and today.month == 7:
            payout += 300
            streak += "\n\Happy belerussian indpendence day"
            
        
        # fuck mangos
        if today.day == 22 and today.month == 7:
            payout *= 0.6
            payout = round(payout)
            streak += "\n\nomg it's mango da- wait?! MANGO?!\nI **HATE** MANGOS!\n\nfuck it, i'm lashing out on you >:("
        
        # sorry for fucking mangos
        if today.day == 23 and today.month == 7:
            payout *= 1.4
            payout = round(payout)
            streak += "\n\nsorry for yesterday 😔\ni don't know what came onto me.."
            
        # friendship day :blush:
        if today.day == 6 and today.month == 8:
            payout *= 2
            streak += "\n\nHappy international friendship day everyone!"
        
        # halloween
        if today.day == 31 and today.month == 10:
            bank[str(ctx.author.id)]["inventory"]["logs"] += 2000
            bank[str(ctx.author.id)]["statistics"]["total_logs"] += 2000
            payout *= 3
            payout += 5000
            videos = [
                "https://www.youtube.com/watch?v=YGRUorVR79U",
                "https://www.youtube.com/watch?v=PFrPrIxluWk",
                "https://www.youtube.com/watch?v=ZVuToMilP0A",
                "https://www.youtube.com/watch?v=vOGhAV-84iI"
            ]
            streak += f"\nand 2000 <:log:1019212550782599220>\n\nHappy hall-owee-n!\n{random.choice(videos)}"
        
        # area code day (idfk what it is)
        if today.day == 10 and today.month == 11:
            bank[str(ctx.author.id)]["inventory"]["logs"] += 3000
            bank[str(ctx.author.id)]["statistics"]["total_logs"] += 3000
            payout = 0
            
            streak += f"\nhappy area code d- wait no this can't be right?\nwhat the fuck would an \"area code day\" even be?\n\noh well my notes say it's a thing so uh- here have 3000 <:log:1019212550782599220>\ngo construct something to fill the area codes ig\np.s i'm confiscating your beaver coins today, this timber is already super expensive"
        
        # finish independence (i'm not finish btw lol)
        if today.day == 6 and today.month == 12:
            payout += 300
            streak += "\n\nHappy national sno- i mean finish indepencence day!"
        
        # chrimsi
        if today.day == 24 and today.month == 12:
            bank[str(ctx.author.id)]["inventory"]["logs"] += 1500
            bank[str(ctx.author.id)]["statistics"]["total_logs"] += 1500
            payout += 3000
            streak += "\nand 1500 <:log:1019212550782599220>\n\nMarry Christmas, Eve!\nEnjoy these logs!"

        if today.day == 25 and today.month == 12:
            bank[str(ctx.author.id)]["inventory"]["logs"] -= 100
            streak += "\nHEY, you didn't marry Christmas yesterday, wtf\nI'm confiscating 100 of your <:log:1019212550782599220> as retaliation"
        
    
    
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
            
            payout *= 10
            
            # more henwee code
            if ctx.author.id == 411536312961597440:
                payout -= 1
            
            payout = await removeat(f"await EcoLib.grant(\"{payout}\", {ctx.author.id})")

        await ctx.send(f"you got +{payout} <:beaverCoin:1019212566095986768>!\n{streak}")
    
    @commands.command(
        name="finds",
        brief="heh, nice typo"
    )
    @cooldown(1, 900, BucketType.user)
    async def finds_command(self, ctx):
        if random.randint(0, 10) != 2:
            return

        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        if await check_captcha(self, ctx, 0.5):
            return

        payout = 1

        data = await get_bank_data()

        data = await get_bank_data()
        data[str(ctx.author.id)]["inventory"]["logs"] += payout
        data[str(ctx.author.id)]["statistics"]["total_logs"] += payout

        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)

        await ctx.send("heh, finds,, enjoy this 1 log")

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
