import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import json
import math
import os
import random
import asyncio
from datetime import datetime


shop = [
  #{"icon":"🕵️️","name":"hacker","shopname":"hacker man","price":750,"description":"slightly increases the money from begging"}, 
  #{"icon":"🕵️️","name":"hacker","shopname":"hacker man","price":750,"description":"slightly increases the money from begging"}, 
  #{"icon":"🕵️️","name":"hacker","shopname":"hacker man","price":750,"description":"slightly increases the money from begging"},
  {"icon":"🕵️️","name":"soon","shopname":"i'll add it sooner or later","price":999999999999999999999999999999999999999999999999,"description":"slightly increases the money from begging"}
  ]

black_holes = [
  {"icon":"<:black_hole1:891359657443070013>","name":"hole1","shopname":"test","price":50000000000,"description":"increases the amount gained from researching"}, 
  {"icon":"<:black_hole2:891363979195191426>","name":"hole2","shopname":"test","price":75000000000,"description":"gives you +4,888,888,888 coins/hour"}, 
  {"icon":"<:black_hole3:891364006252675112>","name":"hole3","shopname":"test","price":200000000000,"description":"gives you +13,153,000,000 coins/hour"}, 
  {"icon":"<:black_hole4:891364058866016317>","name":"hole4","shopname":"test","price":400000000000,"description":"gives you +27,000,000,000 coins/hour"},
  {"icon":"<:black_hole5:891364070131916831>","name":"hole5","shopname":"test","price":5000000000000,"description":"gives you +234,567,654,321 coins/hour"}
]

dark_matter = [
  {"icon":"<:dark_matter1:891354659330084914>","name":"matter1","shopname":"matter1","price":5000000000,"description":"increases the amount gained from researching"}, 
  {"icon":"<:dark_matter2:891354672550535178>","name":"matter2","shopname":"test","price":7500000000,"description":"gives you +474,474,474 coins/hour"}, 
  {"icon":"<:dark_matter3:891354685108285490>","name":"matter3","shopname":"test","price":20000000000,"description":"gives you +1,273,888,888 coins/hour\n not found"}, 
  {"icon":"<:dark_matter4:891354694725816340>","name":"matter4","shopname":"test","price":40000000000,"description":"gives you +2,567,000,000 coins/hour"},
  {"icon":"<:dark_matter5:891354705907810384>","name":"matter5","shopname":"test","price":100000000000,"description":"unlocks the **final** shop\ngives you +6,450,000,000 coins/hour"}
]

alien_slaves = [
  {"icon":"<:alien1:891350767515082754>","name":"alien1","shopname":"alien_slaves","price":500000000,"description":"increases the amount gained from researching"}, 
  {"icon":"<:alien2:891350776037916743>","name":"alien2","shopname":"test","price":750000000,"description":"gives you +47,474,747 coins/hour\n istg this better be worth it"}, 
  {"icon":"<:alien3:891350788029423617>","name":"alien3","shopname":"test","price":2000000000,"description":"gives you +125,125,125 coins/hour"}, 
  {"icon":"<:alien4:891350797416292352>","name":"alien4","shopname":"test","price":4000000000,"description":"gives you +252,252,252 coins/hour"},
  {"icon":"<:alien5:891350806899601489>","name":"alien5","shopname":"test","price":10000000000,"description":"unlocks new shop\ngives you +629,926,000 coins/hour"}
]

stars = [
  {"icon":"<:star1:891346892347306036>","name":"star1","shopname":"stars","price":50000000,"description":"increases the amount gained from researching"}, 
  {"icon":"<:star2:891347232165613598>","name":"star2","shopname":"test","price":75000000,"description":"gives you +4,680,000 coins/hour"}, 
  {"icon":"<:star3:891348527626735617>","name":"star3","shopname":"test","price":200000000,"description":"gives you +12,500,000 coins/hour"}, 
  {"icon":"<:star4:891348573785038920>","name":"star4","shopname":"test","price":400000000,"description":"gives you +25,000,000 coins/hour"},
  {"icon":"<:star5:891349678480850984>","name":"star5","shopname":"test","price":1000000000,"description":"unlocks new shop\ngives you +62,555,555 coins/hour"}
]

planets = [
  {"icon":"<:planet1:891345213476462644>","name":"planet1","shopname":"take control of venus","price":5000000,"description":"increases the amount gained from researching"}, 
  {"icon":"<:planet2:891345255209766973>","name":"planet2","shopname":"how about mars tho?","price":7500000,"description":"gives you +466,466 coins/hour"}, 
  {"icon":"<:planet3:891345781364232212>","name":"planet3","shopname":"hows jupiter?","price":20000000,"description":"gives you +1,234,567 coins/hour\noooooo spicy number"}, 
  {"icon":"<:planet4:891345793322205244>","name":"planet4","shopname":"how about **you're mom**","price":40000000,"description":"gives you +2,469,134 coins/hour"},
  {"icon":"<:planet5:891345808706908190>","name":"planet5","shopname":"ring go spin spin","price":100000000,"description":"unlocks new shop\ngives you +6,234,567 coins/hour"}
]

comets = [
  {"icon":"<:comet1:891343845948784691>","name":"comet1","shopname":"comets","price":500000,"description":"increases the amount gained from reasearching"}, 
  {"icon":"<:comet2:891343902529949716>","name":"comet2","shopname":"test","price":750000,"description":"gives you +46,464 coins/hour"}, 
  {"icon":"<:comet3:891343916987740180>","name":"comet3","shopname":"test","price":2000000,"description":"gives you +123,456 coins/hour"}, 
  {"icon":"<:comet4:891342442585001984>","name":"comet4","shopname":"test","price":4000000,"description":"gives you +249,999 coins/hour"},
  {"icon":"<:comet5:891343845697134592>","name":"comet5","shopname":"moon comet","price":10000000,"description":"wait we made the moon into a heccin comet????\nunlocks new shop\ngives you +626,626 coins/hour"}
]

space_stations = [
  {"icon":"<:space_station1:891115039078109254>","name":"station1","shopname":"when you go spin around sphere","price":50000,"description":"increases the amount gained from researching"}, 
  {"icon":"<:space_station2:891115920091668551>","name":"station2","shopname":"but what if we had multiple things spinning around sphere","price":75000,"description":"gives you +4554 coins/hour"}, 
  {"icon":"<:space_station3:891116003264712754>","name":"station3","shopname":"astronauts can like, exist now","price":200000,"description":"gives you +12,345 coins/hour"}, 
  {"icon":"<:space_station4:891116129404198932>","name":"station4","shopname":"wait when did we go to the moon?","price":400000,"description":"gives you +25,000 coins/hour"}, 
  {"icon":"<:space_station5:891116129630707783>","name":"station5","shopname":"straight up a death star","price":1000000,"description":"unlocks new shop\ngives you +77,777 coins/hour"}
]

satelites = [
  {"icon":"<:satellite1:891107674253582347>","name":"satellite1","shopname":"the first of it\'s kind","price":5000,"description":"gives you a bit more from researching"}, 
  {"icon":"<:satellite2:891107674295504926>","name":"satellite2","shopname":"you want gps?","price":7500,"description":"gives you +400 coins/hour"}, 
  {"icon":"<:satellite3:891107729438044160>","name":"satellite3","shopname":"how about knowing the weather a week in advance","price":20000,"description":"gives you +1111 coins/hour"}, 
  {"icon":"<:satellite4:891107762392670289>","name":"satellite4","shopname":"how about knowing the weather a year in advance","price":40000,"description":"gives you +2345 coins/hour"},
  {"icon":"<:satellite5:891107774002507776>","name":"satellite5","shopname":"how about being able to spy on every single person on earth at all times :)","price":100000,"description":"unlocks new shop\ngives you +5885 coins/hour"}
]

rockets = [
  {"icon":"<:rocket1:891054951755825192>","name":"rocket1","shopname":"Basic rocket","price":50,"description":"slightly increases the amount of money gained from researching"}, 
  {"icon":"<:rocket2:891054952435310702>","name":"rocket2","shopname":"that went poorly, trying again","price":100,"description":"gives you +5 coins/hour"}, 
  {"icon":"<:rocket3:891054952565329940>","name":"rocket3","shopname":"a bit better this time","price":500,"description":"gives you +20 coins/hour"}, 
  {"icon":"<:rocket4:891054953018306611>","name":"rocket4","shopname":"next time you'll get it","price":2000,"description":"gives you +90 coins/hour"},
  {"icon":"<:rocket5:891054989051592724>","name":"rocket5","shopname":"into orbit","price":10000,"description":"unlocks new shop\ngives you +500 coins/hour"}
]



Galaxies = [
  {"icon":":)","name":"placeholder","shopname":"placeholder","price":10000000000000000000000000,"description":"gives +5 coins/day"}
]

rocket1_payouts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,4,6,7,7,7,8,8,8,9,10]


comet1_payouts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5354,1932,1942,9051,6384,8025,6227,6795,7471,5829,15931,129533,31492,29104,12485,25912,90472,1405002,1708020,3050200,4002002,2400000,9600000]


hacker_payouts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,3,3,3,4,5,6,9]

level2_hacker_payouts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,5,6,7,10]

level3_hacker_payouts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,4,5,5,6,6,6,7,11]

upgrades = [
  #{"icon":"<:benjaaaaaamin:890628865276395530>","name":"1","shopname":"1 | benjamin's recruitment","price":3000,"description":"sliiiightly upgrades your hackers"},
  #{"icon":"<:hacker:890644794483826688>","name":"2","shopname":"2 | anonymous","price":16000,"description":"increases your hacker's earnings even more"},
  #{"icon":"<:benjaaaaaaaaaaaaaaaaaaaaaaaaaaaa:890629753223143525>","name":"3","shopname":"3 | benjaaaaamin's jams","price":5000,"description":"lets you have 5 more hackers"},
  #{"icon":"🧑‍💻","name":"4","shopname":"4 | into the matrix","price":12000,"description":"lets you have an extra extra 5 more hackers"},
  #{"icon":"<a:hackerman:890644793695293502>","name":"5","shopname":"5 | get intel on the FBI database","price":25000,"description":"inspires even more hackers to join you, you can get 5 more hackers"}
  {"icon":"<a:hackerman:890644793695293502>","name":"5","shopname":"i\'m going to re add these soon-ish, dw'","price":99999999999999999999999,"description":"bro trust me"}
]




possible_givers = [
  "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone","someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someoen", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "someone", "andromeda", "your future self", "avery, for some reason", "Justin beaver", "rick astley", "queen elizabeth", "spongebob", "memecat", "bob ross", "your mother in law", "i", "your arabic uncle", "your poor mother", "mee6", "dyno", "jeffery bezzzzozz"
]

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tutorial", aliases = ["start", "tut", "economy"], brief = "tells you the basics of the economy system")
    @cooldown(10, 200, BucketType.user)
    async def tutorial_command(self, ctx, page = 1):
        embed = discord.Embed(title = f"yeah as if", description = f"find it our yourself idiot", colour = ctx.author.colour)
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
        embed.add_field(name = "balance", value = f"<:beaverCoin:968588341291397151> {int(wallet_amount)}", inline=False)

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

        with open("data/bank.json", "w") as f:
            json.dump(users, f)
        
        return True


    @commands.Cog.listener()
    async def get_bank_data(self):
        with open("data/bank.json", "r") as f:
            users = json.load(f)
        
        return users

    @commands.Cog.listener()
    async def update_bank_data(self, user, change = 0):
        users = await self.get_bank_data()

        users[str(user.id)]["wallet"] += change

        with open("data/bank.json", "w") as f:
            json.dump(users, f)

        bal = [users[str(user.id)]["wallet"]]
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
