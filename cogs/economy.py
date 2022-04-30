import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import json
import time
import random
import asyncio
from datetime import datetime


class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tutorial", aliases = ["start", "tut", "economy"], brief = "tells you the basics of the economy system")
    @cooldown(10, 200, BucketType.user)
    async def tutorial_command(self, ctx, page = 1):
        embed = discord.Embed(title = f"yeah as if", description = f"find it out yourself idiot", colour = ctx.author.colour)
        await ctx.send(embed = embed)
        return
    
        embed = discord.Embed(title = f"Tutorial Page: {page}", description = f"use `{ctx.prefix}tutorial [page]` to switch pages!", colour = ctx.author.colour)
        if page == 1:
            embed.add_field(name = f"what is this?", value = f"this is the Andromeda economy system, very much based on spaaaaaaaaaaaaaaaaaaaaaaaaaace", inline = False)
            embed.add_field(name = f"how can i get started?", value = f"well, it\'s simple, just go to the 2nd page of this tutorial and we\'ll get started", inline = False)
            embed.add_field(name = f"note", value = f"this is still in early access and pretty much everything is subject to change", inline = False)

        elif page == 2:
            embed.add_field(name = f"The atlas", value = "here you can find the different categories of commands", inline = False)
            embed.add_field(name = f"Page 1: Starting help", value = "tells any newcomers what this is", inline = False)
            embed.add_field(name = f"Page 2: The atlas", value = "you are here, this is where you can find the major categories of commands", inline = False)
            embed.add_field(name = f"Page 3: How to earn money", value = "this page will tell you most of the ways you can earn some shiny <:beaverCoin:968588341291397151>", inline = False)
            #embed.add_field(name = f"Page 4: Upgrades", value = "Upgrades that permanently incrase your production is some sort of way", inline = False)
            #embed.add_field(name = f"Page 5: Gambling", value = "coming soon", inline = False)
        

        elif page == 3:
            embed.add_field(name = f"how to get that cash money", value = f"this is the different ways you can persue to get that bank, gamers", inline = False)
            embed.add_field(name = f"Researching", value = f"simply do {ctx.prefix}research, {ctx.prefix}res, or {ctx.prefix}beg - and you'll get free money", inline = False)
            embed.add_field(name = f"Buying shit", value = f"By using {ctx.prefix}shop you can find many different shops you can use, all of which either buff your hourly automatic cash generation, or increases the amount gained from researching", inline = False)
            embed.add_field(name = f"Gambling :)))", value = f"if you don't really care how much money you would like, you can gamble with commands such as {ctx.prefix}slots and you'll get some <:beaverCoin:968588341291397151> every now and again", inline = False)

        else:
            embed.add_field(name = f"entity not found", value = "try a different page", inline = False)


        embed.set_footer(text=f"page {page} of 3")
        await ctx.send(embed = embed)
        
        
        
    @commands.command(name="slot", aliases=["slots"], brief="do you ever wish you didn\'t have any money? well do i have the solution for YOU, introducing - gambling™")
    @cooldown(1, 5, BucketType.user)
    async def slot_machine_command(self, ctx, amount = None):
        await self.open_account(ctx.author)

        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to waste")
            return

        bal = await self.update_bank_data(ctx.author)

        amount = int(amount)
        if amount > 50000:
            amount = 50000

        if amount > bal[0]:
            await ctx.send("you don\'t have THAT much money")
            return

        if amount < 3:
            await ctx.send("please bet at leaaaast 3 <:beaverCoin:968588341291397151>")
            return

        if amount < 0:
            await ctx.send("sorry, you have to gamble a positive amount of money")
            return

        
        final = []

        slot1 = "<a:slots:849627985857871912>"
        slot2 = "<a:slots:849627985857871912>"
        slot3 = "<a:slots:849627985857871912>"

        msg = await ctx.send(str(final)[:-2]+(str(slot1))+(str(slot2))+(str(slot3)))
        await asyncio.sleep(2)

        slot1 = random.choice([
            "<:Coal:848602311659618315>",
            "<:Redstone:848604340658241576>",
            "<:Iron:848602645207842846>",
            "<:Gold:848602678031548427>",
            "<:Emerald:848602691337060412>",
            "<:Diamond:848602702132019210>"
            ])
        final.append(slot1)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")
        await asyncio.sleep(1.5)
       
        slot2 = random.choice([
          "<:Coal:848602311659618315>",
          "<:Redstone:848604340658241576>",
          "<:Iron:848602645207842846>",
          "<:Gold:848602678031548427>",
          "<:Emerald:848602691337060412>",
          "<:Diamond:848602702132019210>"
          ])
        final.append(slot2)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")
        await asyncio.sleep(1.5)

        slot3 = random.choice([
          "<:Coal:848602311659618315>",
          "<:Redstone:848604340658241576>",
          "<:Iron:848602645207842846>",
          "<:Gold:848602678031548427>",
          "<:Emerald:848602691337060412>",
          "<:Diamond:848602702132019210>"
          ])
        final.append(slot3)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")


        

        if final[0] == "<:Diamond:848602702132019210>" and final[1] == "<:Diamond:848602702132019210>" and final[2] == "<:Diamond:848602702132019210>":
            await self.update_bank_data(ctx.author, 19*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {20*amount} <:beaverCoin:968588341291397151>")

        elif final[0] == "<:Emerald:848602691337060412>" and final[1] == "<:Emerald:848602691337060412>" and final[2] == "<:Emerald:848602691337060412>":
            await self.update_bank_data(ctx.author, 9*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {10*amount} <:beaverCoin:968588341291397151>")

        elif final[0] == "<:Gold:848602678031548427>" and final[1] == "<:Gold:848602678031548427>" and final[2] == "<:Gold:848602678031548427>":
            await self.update_bank_data(ctx.author, 13*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {14*amount} <:beaverCoin:968588341291397151>")

        elif final[0] == "<:Iron:848602645207842846>" and final[1] == "<:Iron:848602645207842846>" and final[2] == "<:Iron:848602645207842846>":
            await self.update_bank_data(ctx.author, 6*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {7*amount} <:beaverCoin:968588341291397151>")

        elif final[0] == "<:Redstone:848604340658241576>" and final[1] == "<:Redstone:848604340658241576>" and final[2] == "<:Redstone:848604340658241576>":
            await self.update_bank_data(ctx.author, 5*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {6*amount} <:beaverCoin:968588341291397151>")

        elif final[0] == "<:Coal:848602311659618315>" and final[1] == "<:Coal:848602311659618315>" and final[2] == "<:Coal:848602311659618315>":
            await self.update_bank_data(ctx.author, 4*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {5*amount} <:beaverCoin:968588341291397151>")
        
        elif final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            await self.update_bank_data(ctx.author, 0.5*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {1.5*amount} <:beaverCoin:968588341291397151>")

        else:
            await self.update_bank_data(ctx.author, -1*amount, "wallet")
            await ctx.send(f"<:sadcat:849342846582390834> - {ctx.author.display_name} lost {amount} <:beaverCoin:968588341291397151>")




    @commands.command(name="sell", brief="try selling your useless items")
    @cooldown(3, 10, BucketType.user)
    async def sell_command(self, ctx):
        await ctx.send("lmao no")


    @commands.command(name="inventory", aliases=["inv", "items"], brief="lets you check your items n\' stuff")
    @cooldown(1, 3, BucketType.user)
    async def inv_command(self, ctx, user: discord.Member = None):
        
        if user is None:
            user = ctx.author

        n = 0
        
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        items = await self.get_items_data()

        try:
            inv = users[str(user.id)]["inventory"]
        except:
            inv = []


        embed = discord.Embed(title=f"{user.display_name}'s Inventory", color=ctx.author.color)

        for item in inv:
            for i in items:
                if item == i:
                    embed.add_field(name=f"{items[i][0]} {items[i][1]}" , value=f"{inv[item]}", inline=False)
                    n += 1
        
        if n == 0:
            embed.add_field(name="Empty", value=f"{user.display_name} does not have any items in their inventory", inline=False)
        


        await ctx.send(embed = embed)
    
    
    @commands.command(name="profile", brief="tells you some basic info about the person specified")
    @cooldown(3,10, BucketType.user)
    async def generateprofile(self, ctx, user : discord.Member = None):

        if user is None:
            user = ctx.author
            
        await self.open_account(user)

        bankdata = await self.get_bank_data()
            
        wallet_amount = bankdata[str(user.id)]["wallet"]

        embed = discord.Embed(title = f"", colour = ctx.author.colour, timestamp=datetime.utcnow())
        embed.add_field(name = f"{user.display_name}", value = f"placeholder", inline=False)
        embed.add_field(name = "Balance:", value = f"<:beaverCoin:968588341291397151> {int(wallet_amount)}", inline=False)
        
        married_to_data = bankdata[str(user.id)]["marriage"]
        married_to = ""
        n = 0
        y = 0
        for i in married_to_data:
            if n < 5:
                x = await self.bot.fetch_user(i)
                married_to += str(x.display_name) + "\n"
                n += 1
                
            else:
                y += 1
        if y != 0:
            married_to += f"and {y} more"
            
        embed.add_field(name = "Married to:", value = f"{married_to}", inline=False)

        embed.set_footer(text="Sent from my iPhone"),
        embed.set_thumbnail(url=f"{user.avatar_url}")

        await ctx.send(embed = embed)



    @commands.command(name="balance", aliases=["bank","bal","money"], brief="check your current balance")
    @cooldown(2, 10, BucketType.user)
    async def check_balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        await self.open_account(user)

        users = await self.get_bank_data()

        wallet_amount = users[str(user.id)]["wallet"]

        embed = discord.Embed(title = f"{user.display_name}'s balance", colour = ctx.author.colour)
        embed.add_field(name = "wallet balance", value = f"{wallet_amount} <:beaverCoin:968588341291397151>")
        await ctx.send(embed = embed)




    @commands.command(name="leaderboard", aliases=["lb", "top"], brief="checks the current leaderboard")
    @cooldown(2, 10, BucketType.user)
    async def leaderboard_command(self, ctx, x = 5):
        users = await self.get_bank_data()
        if x > 10:
            x = 10
        
        leaderboard = []
        
        for user in users:
            leaderboard.append([user, users[user]["wallet"]])
        
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(title = f"Top {x} richest people", colour = ctx.author.colour)
        
        for i in range(0, x):
            try:
                user = await self.bot.fetch_user(int(leaderboard[i][0]))
                balance = leaderboard[i][1]
                embed.add_field(name = f"{i+1}. {user.display_name}", value = f"{balance} <:beaverCoin:968588341291397151>", inline=False)
            except Exception as e:
                await ctx.send(f"error: {e}")
                break
        
        await ctx.reply(embed = embed, mention_author = False)

    @commands.command(name="send", aliases=["give", "simp", "transfer", "gift"], brief="give someone money, you simp :)")
    @cooldown(2, 10, BucketType.user)
    async def send_command(self, ctx, member:discord.Member, amount = None):
        await self.open_account(ctx.author)
        await self.open_account(member)

        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to give <:shy:848650912636600320>")
            return

        bal = await self.update_bank_data(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("you don\'t have THAT much money, jeezzzz")
            return

        if amount < 0:
            await ctx.send("sorry, you sadly can\'t to give a negative amount of money <:smh:848652740250828821>")
            return

        await self.update_bank_data(ctx.author, -1*amount)
        await self.update_bank_data(member, amount)

        await ctx.send(f"{ctx.author.display_name} gave {amount} <:beaverCoin:968588341291397151> to {member.display_name}")

    
    
    @commands.command(name = "shop", brief = "buy something, wouldya?")
    @cooldown(3, 15, BucketType.user)
    async def shop_command(self, ctx):
        await self.open_account(ctx.author)
        
        shop = await self.get_shop_data()
        
        embed = discord.Embed(title = "Shop", description = "buy something, wouldya?", colour = ctx.author.colour)
        
        for i in shop:
            embed.add_field(name = f"{i} {shop[i][1]}", value = f"{shop[i][0]} <:beaverCoin:968588341291397151>", inline=False)

        await ctx.send(embed = embed)
    
    @commands.command(name = "buy", brief = "pay for something, wouldya?")
    @cooldown(3, 15, BucketType.user)
    async def buy_command(self, ctx, *, item):
        await self.open_account(ctx.author)
        
        shop = await self.get_shop_data()
        bank = await self.get_bank_data()
        wallet = bank[str(ctx.author.id)]["wallet"]
        
        for i in shop:
            if item.lower() == i.lower():
                if wallet < shop[i][0]:
                    await ctx.send("you don't have enough money to buy that")
                    return

                try:
                    bank[str(ctx.author.id)]["inventory"][item.lower()] += 1
                except:
                    bank[str(ctx.author.id)]["inventory"][item.lower()] = 1
                
                bank[str(ctx.author.id)]["wallet"] -= shop[i][0]
                    
                with open("data/bank.json", "w") as f:
                    json.dump(bank, f)

                await ctx.send(f"You just bought {shop[i][1]} for {shop[i][0]} <:beaverCoin:968588341291397151>")
                return
        
        await ctx.send("i could not find that item, sorry")
    
    @commands.command(name = "daily", brief = "get your daily beaver coins here!")
    @cooldown(3, 15, BucketType.user)
    async def daily_command(self, ctx):
        await self.open_account(ctx.author)
        
        bank = await self.get_bank_data()
        daily_info = bank[str(ctx.author.id)]["daily"]
                
        if daily_info["day"] == (datetime.utcnow() - datetime(1970,1,1)).days:
            return await ctx.send("you already got your daily, come back tomorrow")
        
        streak = ""
        if daily_info["streak"] != 0 and daily_info["day"] < (datetime.utcnow() - datetime(1970,1,1)).days - 1:
            daily_info["streak"] = 0
            streak += f"you lost your streak of {daily_info['streak']} days!\n"
        
        else:
            daily_info["streak"] += 1
            streak += f"you got your daily {daily_info['streak']} days in a row!"
          
        payout = random.randint(25, 75) + round(random.randrange(5,10) * daily_info["streak"])
        if payout >= 500:
            payout = 500
        
        bank[str(ctx.author.id)]["wallet"] += payout
        daily_info["day"] = (datetime.utcnow() - datetime(1970,1,1)).days
        bank[str(ctx.author.id)]["daily"] = daily_info
        with open("data/bank.json", "w") as f:
            json.dump(bank, f)
        
        
        await ctx.send(f"you got {payout} <:beaverCoin:968588341291397151>!\n{streak}")
        
    #########################################
    #########################################
    ############ M A R R I A G E ############
    #########################################
    #########################################
    
    #this code doesn't use any else statements btw 😎 i find it more clean :shrug:
    @commands.command(name = "marry")
    @cooldown(20, 600, BucketType.user)
    async def react_henwee(self, ctx, member:discord.Member):
        if member == None or member == ctx.author or member.bot:
            await ctx.send("please tell me who you want to marry")
            return

        await self.open_account(ctx.author)
        data = await self.get_bank_data()
        if member.id in data[str(ctx.author.id)]["marriage"]:
            await ctx.send(f"you're already married to {member.display_name}")
            return
        
        await self.open_account(member)

        try:
            if data[str(ctx.author.id)]["inventory"]["ring"] <= 0:
                await ctx.send(f"you do not have any rings 💍 to give {member.mention}")
                return
        except:
            await ctx.send(f"you do not have any rings 💍 to give {member.mention}")
            return
        
        await ctx.send(f"alright, {ctx.author.mention}, are you sure you want to marry {member.mention}? your ring 💍 will disentegrate if you do")
        response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=20)
        confirmations = ["yes", "yep", "yup", "y", "correct", "ys", "ye"]
        if response.content.lower() not in confirmations:
            await ctx.send(f"apparently {ctx.author.mention} doesn't want to marry {member.mention} afterall")
            return
        
        await ctx.send(f"alright then, {member.mention}, do you wish to marry {ctx.author.mention}?")
        member_response = await self.bot.wait_for("message", check=lambda m: m.author == member, timeout=20)
        if member_response.content.lower() not in confirmations:
            await ctx.send(f"{member.mention} did not want to marry {ctx.author.mention}, what a shame")
            return
        
        await ctx.send(f"it's a match! {ctx.author.mention} and {member.mention} are now married!! 🥳🥳\nyour marriage will now appear on both of your profiles")
        
        data = await self.get_bank_data()
        data[str(ctx.author.id)]["inventory"]["ring"] -= 1
        data[str(ctx.author.id)]["marriage"].append(member.id)
        data[str(member.id)]["marriage"].append(ctx.author.id)
        
        with open("data/bank.json", "w") as f:
            json.dump(data, f)
        
    
    #########################################
    #########################################
    #### E V E N T     F U N C T I O N S ####
    #########################################
    #########################################
    
    
    
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        
        await self.open_account(ctx.author)
        
        data = await self.get_bank_data()
        
        loaded_time = data[str(ctx.author.id)]["speak_cooldown"]
        
        if loaded_time < time.time():
            data[str(ctx.author.id)]["speak_cooldown"] = time.time() + 450 + random.randint(0,150)
            with open("data/bank.json", "w") as f:
                json.dump(data, f)
             
            
            await self.update_bank_data(ctx.author, random.randint(2,5))
            await self.update_bank_data(ctx.author, 1, "xp")
            
        
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        print(user)
        
        await self.open_account(user)
        
        data = await self.get_bank_data()
        
        loaded_time = data[str(user.id)]["speak_cooldown"]
        
        if loaded_time < time.time():
            data[str(user.id)]["speak_cooldown"] = time.time() + 450 + random.randint(0,150)
            with open("data/bank.json", "w") as f:
                json.dump(data, f)
             
            
            await self.update_bank_data(user, random.randint(2,5))
            await self.update_bank_data(user, 1, "xp")
        
        
    ###########################################
    ###########################################
    #### H E L P E R     F U N C T I O N S ####
    ###########################################
    ###########################################

    
    @commands.Cog.listener()
    async def get_items_data(self):
        with open("data/items.json", "r") as f:
            items = json.load(f)
        
        return items
    
    @commands.Cog.listener()
    async def get_shop_data(self):

        with open("data/shop.json", "r") as f:
            shop = json.load(f)
        
        return shop
        
    @commands.Cog.listener()
    async def open_account(self, user):

        users = await self.get_bank_data()

        try:
            (users[str(user.id)]["inventory"])
            
        except:
            if str(user.id) in users:
                users[str(user.id)]["inventory"] = {}
                with open("data/bank.json", "w") as f:
                    json.dump(users, f)
                
        
        users = await self.get_bank_data()
        
        try:
            (users[str(user.id)]["daily"])
            
        except:
            if str(user.id) in users:
                users[str(user.id)]["daily"] = {}
                with open("data/bank.json", "w") as f:
                    json.dump(users, f)
                
                return
                
        if str(user.id) in users:
            return


        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 10.0
        users[str(user.id)]["xp"] = 0
        users[str(user.id)]["speak_cooldown"] = time.time() + 300
        users[str(user.id)]["marriage"] = []
        users[str(user.id)]["inventory"] = {}
        users[str(user.id)]["daily"] = {}
        users[str(user.id)]["daily"]["day"] = 0
        users[str(user.id)]["daily"]["streak"] = 0

        with open("data/bank.json", "w") as f:
            json.dump(users, f)
        
        return True


    @commands.Cog.listener()
    async def get_bank_data(self):
        with open("data/bank.json", "r") as f:
            users = json.load(f)
        
        return users

    @commands.Cog.listener()
    async def update_bank_data(self, user, change = 0, mode = "wallet"):
        users = await self.get_bank_data()

        users[str(user.id)][mode] += change

        with open("data/bank.json", "w") as f:
            json.dump(users, f)

        bal = [users[str(user.id)][mode]]
        return bal


def setup(bot):
    bot.add_cog(economy(bot))
