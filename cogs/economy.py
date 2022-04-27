import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import json
import time
import random
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
            
        

    @commands.command(name="sell", brief="try selling your useless items")
    @cooldown(3, 10, BucketType.user)
    async def sell_command(self, ctx):
        await ctx.send("lmao no")


    @commands.command(name="inventory", aliases=["inv", "items"], brief="lets you check your items n\' stuff")
    @cooldown(1, 3, BucketType.user)
    async def inv_command(self, ctx, user: discord.Member = None):
        
        if user is None:
            user = ctx.author

        await self.open_account(ctx.author)
        users = await self.get_bank_data()

        try:
            inv = users[str(user.id)]["inv"]
        except:
            inv = []


        em = discord.Embed(title = "Inventory")
        for item in inv:
            icon = item["icon"]
            name = item["item"]
            amount = item["amount"]

            em.add_field(name = icon + name, value = amount)    

        await ctx.send(embed = em)
    
    
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
        
        embed.add_field(name = "Married to:", value = f"no one", inline=False)

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
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total,reverse=True)    

        em = discord.Embed(title = f"Top {x} Richest People" , description = "this is decided based on the amount of money in the person\'s bank and wallet combined",color = discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.bot.get_user(id_)
            name = member.name
            em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed = em)


    @commands.command(name="send", aliases=["give", "simp", "transfer", "gift"], brief="puts money from your wallet into your bank")
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

        await ctx.send(f"{ctx.author.display_name} gave {amount} <:beaverCoin:968588341291397151> to s{member.display_name}")


    
    #########################################
    #########################################
    #### E V E N T     F U N C T I O N S ####
    #########################################
    #########################################
    
    
    
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "a!" in ctx.content or ctx.author.bot: return
        await self.open_account(ctx.author)
        
        data = await self.get_bank_data()
        
        loaded_time = data[str(ctx.author.id)]["speak_cooldown"]
        
        if loaded_time < time.time() - 300:
            await self.update_bank_data(ctx.author, time.time() - loaded_time + random.randint(0,300), "speak_cooldown")
            await self.update_bank_data(ctx.author, 1)
            await self.update_bank_data(ctx.author, 1, "xp")
            
        
        
        
        
        
    ###########################################
    ###########################################
    #### H E L P E R     F U N C T I O N S ####
    ###########################################
    ###########################################


    @commands.Cog.listener()
    async def open_shop(self):

        with open("data/shop.json", "r") as f:
            json.load(f)
        
    @commands.Cog.listener()
    async def open_account(self, user):

        users = await self.get_bank_data()

        if str(user.id) in users:
            return False

        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 10.0
            users[str(user.id)]["xp"] = 0
            users[str(user.id)]["speak_cooldown"] = time.time() + 300
            users[str(user.id)]["marriage"] = []

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

    @commands.Cog.listener()
    async def buy_this(self, user,item_name,amount,shop):
        item_name = item_name.lower()
        name_ = None
        for item in shop:
            name = item["name"].lower()
            if name == item_name:
                icon = item["icon"]
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank_data(user)

        if bal[0]<cost:
            return [False,2]

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["inv"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["inv"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1 
            if t == None:
                obj = {"icon":icon , "item":item_name , "amount" : amount}
                users[str(user.id)]["inv"].append(obj)
        except:
            obj = {"icon":icon , "item":item_name , "amount" : amount}
            users[str(user.id)]["inv"] = [obj]        

        with open("data/bank.json","w") as f:
            json.dump(users,f)

        await self.update_bank_data(user,cost*-1,)

        return [True,"Worked"]


def setup(bot):
    bot.add_cog(economy(bot))
