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
        embed = discord.Embed(title = f"Tutorial Page: {page}", description = f"use `{ctx.prefix}tutorial [page]` to switch pages!", colour = ctx.author.colour)
        if page == 1:
            embed.add_field(name = f"what is this?", value = f"this is the Andromeda economy system, very much based on spaaaaaaaaaaaaaaaaaaaaaaaaaace", inline = False)
            embed.add_field(name = f"how can i get started?", value = f"well, it\'s simple, just go to the 2nd page of this tutorial and we\'ll get started", inline = False)
            embed.add_field(name = f"note", value = f"this is still in early access and pretty much everything is subject to change", inline = False)

        elif page == 2:
            embed.add_field(name = f"The atlas", value = "here you can find the different categories of commands", inline = False)
            embed.add_field(name = f"Page 1: Starting help", value = "tells any newcomers what this is", inline = False)
            embed.add_field(name = f"Page 2: The atlas", value = "you are here, this is where you can find the major categories of commands", inline = False)
            embed.add_field(name = f"Page 3: How to earn money", value = "this page will tell you most of the ways you can earn some shiny <a:spinningspacecoin:891686810328125502>", inline = False)
            #embed.add_field(name = f"Page 4: Upgrades", value = "Upgrades that permanently incrase your production is some sort of way", inline = False)
            #embed.add_field(name = f"Page 5: Gambling", value = "coming soon", inline = False)
        

        elif page == 3:
            embed.add_field(name = f"how to get that cash money", value = f"this is the different ways you can persue to get that bank, gamers", inline = False)
            embed.add_field(name = f"Researching", value = f"simply do {ctx.prefix}research, {ctx.prefix}res, or {ctx.prefix}beg - and you'll get free money", inline = False)
            embed.add_field(name = f"Buying shit", value = f"By using {ctx.prefix}shop you can find many different shops you can use, all of which either buff your hourly automatic cash generation, or increases the amount gained from researching", inline = False)
            embed.add_field(name = f"Gambling :)))", value = f"if you don't really care how much money you would like, you can gamble with commands such as {ctx.prefix}slots and you'll get some <a:spinningspacecoin:891686810328125502> every now and again", inline = False)

        else:
            embed.add_field(name = f"entity not found", value = "try a different page", inline = False)


        embed.set_footer(text=f"page {page} of 3")
        await ctx.send(embed = embed)
            


    @commands.command(name="shop", aliases = ["market", "store"], brief="hire workers for your uhm, totally not coal mine")
    @cooldown(10, 30, BucketType.user)
    async def shop_command(self, ctx, whichone = "Default", user: discord.Member = None):
        if user == None:
            user = ctx.author

        whichone = whichone.lower() 
        users = await self.get_bank_data()

        rocket1amount = rocket2amount = rocket3amount = rocket4amount = rocket5amount = satellite1amount = satellite2amount = satellite3amount = satellite4amount = satellite5amount = station1amount = station2amount = station3amount = station4amount = station5amount = comet1amount = comet2amount = comet3amount = comet4amount = comet5amount = planet1amount = planet2amount = planet3amount = planet4amount = planet5amount = star1amount = star2amount = star3amount = star4amount = star5amount = alien1amount = alien2amount = alien3amount = alien4amount = alien5amount = matter1amount = matter2amount = matter3amount = matter4amount = matter5amount = hole1amount = hole2amount = hole3amount = hole4amount = hole5amount = 0


        try:
            inventory = users[str(user.id)]["inv"]
        except:
            inventory = []

        try:
            upgrades = users[str(user.id)]["upgrd"]
        except:
            upgrades = []

        #await ctx.send(f"{inventory}")

        if whichone == "aliens":
            embed = discord.Embed(title = f"Alien ~~slaves~~ workers", colour = user.colour)

        else:
            embed = discord.Embed(title = f"{whichone.capitalize()}", colour = user.colour)

        for upgrd in upgrades:
            upgradename = upgrd["item"]
                
            if upgradename == "1":
                upgrade1 = "purchased"
            if upgradename == "2":
                upgrade2 = "purchased"
            if upgradename == "3":
                upgrade3 = "purchased"
            if upgradename == "4":
                upgrade4 = "purchased"
            if upgradename == "5":
                upgrade5 = "purchased"


        for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "rocket1":
                    rocket1amount = inventoryitemamount
                elif inventoryitem == "rocket2":
                    rocket2amount = inventoryitemamount
                elif inventoryitem == "rocket3":
                    rocket3amount = inventoryitemamount
                elif inventoryitem == "rocket4":
                    rocket4amount = inventoryitemamount
                elif inventoryitem == "rocket5":
                    rocket5amount = inventoryitemamount

                elif inventoryitem == "satellite1":
                    satellite1amount = inventoryitemamount
                elif inventoryitem == "satellite2":
                    satellite2amount = inventoryitemamount
                elif inventoryitem == "satellite3":
                    satellite3amount = inventoryitemamount
                elif inventoryitem == "satellite4":
                    satellite4amount = inventoryitemamount
                elif inventoryitem == "satellite5":
                    satellite5amount = inventoryitemamount

                elif inventoryitem == "station1":
                    station1amount = inventoryitemamount
                elif inventoryitem == "station2":
                    station2amount = inventoryitemamount
                elif inventoryitem == "station3":
                    station3amount = inventoryitemamount
                elif inventoryitem == "station4":
                    station4amount = inventoryitemamount
                elif inventoryitem == "station5":
                    station5amount = inventoryitemamount

                elif inventoryitem == "comet1":
                    comet1amount = inventoryitemamount
                elif inventoryitem == "comet2":
                    comet2amount = inventoryitemamount
                elif inventoryitem == "comet3":
                    comet3amount = inventoryitemamount
                elif inventoryitem == "comet4":
                    comet4amount = inventoryitemamount
                elif inventoryitem == "comet5":
                    comet5amount = inventoryitemamount

                elif inventoryitem == "planet1":
                    planet1amount = inventoryitemamount
                elif inventoryitem == "planet2":
                    planet2amount = inventoryitemamount
                elif inventoryitem == "planet3":
                    planet3amount = inventoryitemamount
                elif inventoryitem == "planet4":
                    planet4amount = inventoryitemamount
                elif inventoryitem == "planet5":
                    planet5amount = inventoryitemamount

                elif inventoryitem == "star1":
                    star1amount = inventoryitemamount
                elif inventoryitem == "star2":
                    star2amount = inventoryitemamount
                elif inventoryitem == "star3":
                    star3amount = inventoryitemamount
                elif inventoryitem == "star4":
                    star4amount = inventoryitemamount
                elif inventoryitem == "star5":
                    star5amount = inventoryitemamount

                elif inventoryitem == "alien1":
                    alien1amount = inventoryitemamount
                elif inventoryitem == "alien2":
                    alien2amount = inventoryitemamount
                elif inventoryitem == "alien3":
                    alien3amount = inventoryitemamount
                elif inventoryitem == "alien4":
                    alien4amount = inventoryitemamount
                elif inventoryitem == "alien5":
                    alien5amount = inventoryitemamount
                
                elif inventoryitem == "matter1":
                    matter1amount = inventoryitemamount
                elif inventoryitem == "matter2":
                    matter2amount = inventoryitemamount
                elif inventoryitem == "matter3":
                    matter3amount = inventoryitemamount
                elif inventoryitem == "matter4":
                    matter4amount = inventoryitemamount
                elif inventoryitem == "matter5":
                    matter5amount = inventoryitemamount

                elif inventoryitem == "hole1":
                    hole1amount = inventoryitemamount
                elif inventoryitem == "hole2":
                    hole2amount = inventoryitemamount
                elif inventoryitem == "hole3":
                    hole3amount = inventoryitemamount
                elif inventoryitem == "hole4":
                    hole4amount = inventoryitemamount
                elif inventoryitem == "hole5":
                    hole5amount = inventoryitemamount

        if whichone == "shop":
            for item in shop:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                embed.add_field(name = f"{icon} {shopname}", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "rockets" or whichone == "rocket":
            maxupgrade1 = 1
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0
           
            if rocket1amount >= 1:
                maxupgrade1 += 1

            if rocket1amount >= 2:
                maxupgrade1 += 2
                maxupgrade2 += 1

            if rocket1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 2
                maxupgrade4 += 1

            if rocket2amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
                maxupgrade3 += 1

            if rocket2amount >= 10:
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 1

            if rocket3amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if rocket3amount >= 10:
                maxupgrade3 += 5
                maxupgrade4 += 2
          
            if rocket4amount >= 1:
                maxupgrade1 += 4
                maxupgrade2 += 3
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1

            if rocket4amount >= 10:
                maxupgrade4 += 3
            
            if rocket5amount >= 1:
                maxupgrade1 += 7
                maxupgrade2 += 3
                maxupgrade3 += 1
                maxupgrade4 += 1


            for item in rockets:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({rocket1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({rocket2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({rocket3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({rocket4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({rocket5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "satelites" or whichone == "satellite":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

    
            if rocket5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if satellite1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if satellite1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if satellite2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if satellite2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if satellite3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if satellite3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if satellite4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if satellite5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in satelites:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({satellite1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                    #embed.add_field(name = f"{icon} {shopname} `({satellite1amount}/{maxupgrade1})`", value = f"Cost: {price+(price*(0.005+0.0005*(satellite1amount)))**2} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({satellite2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({satellite3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({satellite4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({satellite5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "space_stations" or whichone == "stations":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if satellite5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if station1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if station1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if station2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if station2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if station3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if station3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if station4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if station5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "station1":
                    upgrade1amount = inventoryitemamount
                elif inventoryitem == "station2":
                    upgrade2amount = inventoryitemamount
                elif inventoryitem == "station3":
                    upgrade3amount = inventoryitemamount
                elif inventoryitem == "station4":
                    upgrade4amount = inventoryitemamount
                elif inventoryitem == "station5":
                    upgrade5amount = inventoryitemamount

            for item in space_stations:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({station1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({station2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({station3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({station4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({station5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "comets" or whichone == "astroids" or whichone == "meteors":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if station5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if comet1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if comet1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if comet2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if comet2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if comet3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if comet3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if comet4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if comet5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "comet1":
                    upgrade1amount = inventoryitemamount
                elif inventoryitem == "comet2":
                    upgrade2amount = inventoryitemamount
                elif inventoryitem == "comet3":
                    upgrade3amount = inventoryitemamount
                elif inventoryitem == "comet4":
                    upgrade4amount = inventoryitemamount
                elif inventoryitem == "comet5":
                    upgrade5amount = inventoryitemamount

            for item in comets:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({comet1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({comet2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({comet3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({comet4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({comet5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "planets":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if comet5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if planet1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if planet1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if planet2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if planet2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if planet3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if planet3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if planet4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if planet5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "planet1":
                    upgrade1amount = inventoryitemamount
                elif inventoryitem == "planet2":
                    upgrade2amount = inventoryitemamount
                elif inventoryitem == "planet3":
                    upgrade3amount = inventoryitemamount
                elif inventoryitem == "planet4":
                    upgrade4amount = inventoryitemamount
                elif inventoryitem == "planet5":
                    upgrade5amount = inventoryitemamount

            for item in planets:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({planet1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({planet2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({planet3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({planet4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({planet5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "stars" or whichone == "suns":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if planet5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if star1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if star1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if star2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if star2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if star3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if star3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if star4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if star5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "star1":
                    upgrade1amount = inventoryitemamount
                elif inventoryitem == "star2":
                    upgrade2amount = inventoryitemamount
                elif inventoryitem == "star3":
                    upgrade3amount = inventoryitemamount
                elif inventoryitem == "star4":
                    upgrade4amount = inventoryitemamount
                elif inventoryitem == "star5":
                    upgrade5amount = inventoryitemamount

            for item in stars:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({star1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({star2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({star3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({star4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({star5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "alien_slaves" or whichone == "slaves" or whichone == "aliens":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if star5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if alien1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if alien1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if alien2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if alien2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if alien3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if alien3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if alien4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if alien5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "alien1":
                    upgrade1amount = inventoryitemamount
                elif inventoryitem == "alien2":
                    upgrade2amount = inventoryitemamount
                elif inventoryitem == "alien3":
                    upgrade3amount = inventoryitemamount
                elif inventoryitem == "alien4":
                    upgrade4amount = inventoryitemamount
                elif inventoryitem == "alien5":
                    upgrade5amount = inventoryitemamount

            for item in alien_slaves:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({alien1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({alien2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({alien3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({alien4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({alien5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "dark_matter" or whichone == "matter" or whichone == "darkmatter":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if alien5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if matter1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if matter1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if matter2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if matter2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if matter3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if matter3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if matter4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if matter5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "matter1":
                    upgrade1amount = inventoryitemamount
                elif inventoryitem == "matter2":
                    upgrade2amount = inventoryitemamount
                elif inventoryitem == "matter3":
                    upgrade3amount = inventoryitemamount
                elif inventoryitem == "matter4":
                    upgrade4amount = inventoryitemamount
                elif inventoryitem == "matter5":
                    upgrade5amount = inventoryitemamount

            for item in dark_matter:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({matter1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({matter2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({matter3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({matter4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({matter5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        elif whichone == "black_holes" or whichone == "holes" or whichone == "black" or whichone == "blackholes":
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if matter5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if hole1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if hole1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if hole2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if hole2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if hole3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if hole3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if hole4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if hole5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if maxupgrade1 == 0 and maxupgrade2 == 0 and maxupgrade3 == 0 and maxupgrade4 == 0 and maxupgrade5 == 0:
                embed.add_field(name = f"this shop is empty", value = f"you are yet to unlock it, you'll unlock it after you purchase a certain item", inline = False)

            for item in inventory:
                inventoryitem = item["item"]
                inventoryitemamount = item["amount"]
            
                if inventoryitem == "hole1":
                    upgrade1amount = inventoryitemamount
                elif inventoryitem == "hole2":
                    upgrade2amount = inventoryitemamount
                elif inventoryitem == "hole3":
                    upgrade3amount = inventoryitemamount
                elif inventoryitem == "hole4":
                    upgrade4amount = inventoryitemamount
                elif inventoryitem == "hole5":
                    upgrade5amount = inventoryitemamount

            for item in black_holes:
                icon = item["icon"]
                name = item["name"]
                shopname = item["shopname"]
                price = item["price"]
                description = item["description"]

                if name.endswith("1") and maxupgrade1 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({hole1amount}/{maxupgrade1})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("2") and maxupgrade2 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({hole2amount}/{maxupgrade2})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("3") and maxupgrade3 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({hole3amount}/{maxupgrade3})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("4") and maxupgrade4 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({hole4amount}/{maxupgrade4})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)
                elif name.endswith("5") and maxupgrade5 != 0:
                    embed.add_field(name = f"{icon} {shopname} `({hole5amount}/{maxupgrade5})`", value = f"Cost: {price} <a:spinningspacecoin:891686810328125502>\n{description}\n ID: `{name}`", inline = False)

        else:
            embed.add_field(name = f"this is the default shop", value = "Please select which shop you want to view", inline = False)
            embed.add_field(name = f"{ctx.prefix}shop (what shop you want to view)", value = "shop\nrockets\nsatelites\nspace_stations/stations\ncomets/astroids\nplanets\nstars\naliens\ndarkmatter/matter\nblackholes/holes", inline = False)

        await ctx.send(embed = embed)


    @commands.command(name="upgrades", brief="buy some upgrades i dunnu")
    @cooldown(5,20, BucketType.user)
    async def upgrades_command(self, ctx, page = 1, user: discord.Member = None):
        if user == None:
            user = ctx.author
            
        embed = discord.Embed(title = "Upgrades")
        embed.add_field(name = "how do you upgrade?", value = f"purchase the upgrades with \"{ctx.prefix}upgrade (upgrade ID (see the left part of the embed))", inline = False)

        users = await self.get_bank_data()

        upgrade1 = upgrade2 = upgrade3 = upgrade4 = upgrade5 = "notpurchased"
        
        try:
            checkupgrades = users[str(user.id)]["upgrd"]
        except:
            checkupgrades = []

        for upgrd in checkupgrades:
            upgradename = upgrd["item"]
                
            if upgradename == "1":
                upgrade1 = "purchased"
            if upgradename == "2":
                upgrade2 = "purchased"
            if upgradename == "3":
                upgrade3 = "purchased"
            if upgradename == "4":
                upgrade4 = "purchased"
            if upgradename == "5":
                upgrade5 = "purchased"

        pages = 0
        n = 0

        for item in upgrades:
            pages +=1
           
        for item in upgrades:
            if n < (page*5):
                icon = item["icon"]
                itemid = item["name"]
                name = item["shopname"]
                price = item["price"]
                description = item["description"]
                n += 1

                if n >= (page*5)-5:
                    if itemid == "1":
                        if upgrade1 == "purchased":
                            embed.add_field(name = f"~~{icon} {name}~~", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)
                            upgrade1 = "notpurchased",
                        else:
                            embed.add_field(name = f"{icon} {name}", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)
                    
                    elif itemid == "2":
                        if upgrade2 == "purchased":
                            embed.add_field(name = f"~~{icon} {name}~~", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)
                            upgrade2 = "notpurchased"
                        else:
                            embed.add_field(name = f"{icon} {name}", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)

                    elif itemid == "3":
                        if upgrade3 == "purchased":
                            embed.add_field(name = f"~~{icon} {name}~~", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)
                            upgrade3 = "notpurchased"
                        else:
                            embed.add_field(name = f"{icon} {name}", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)

                    elif itemid == "4":
                        if upgrade4 == "purchased":
                            embed.add_field(name = f"~~{icon} {name}~~", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)
                            upgrade4 = "notpurchased"
                        else:
                            embed.add_field(name = f"{icon} {name}", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)

                    elif itemid == "5":
                        if upgrade5 == "purchased":
                            embed.add_field(name = f"~~{icon} {name}~~", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)
                            upgrade5 = "notpurchased"
                        else:
                            embed.add_field(name = f"{icon} {name}", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)

                    else:
                        embed.add_field(name = f"{icon} {name}", value = f"{price} <a:spinningspacecoin:891686810328125502> | {description}", inline = False)

                    
        embed.set_footer(text=f"page {page} of {int(math.ceil(pages/5))}"),
        await ctx.send(embed = embed)


    @commands.command(name="buy", aliases=["purchase", "aquire", "get"], brief="buy some shit, indulge in capitalism")
    @cooldown(50, 15, BucketType.user)
    async def buy_command(self, ctx, item, amount = 1):
        if amount > 1:
            await ctx.send("sorry, buying multiple copies of an item in the same command is currently disabled.")
            amount = 1

        buyembed = discord.Embed(title = " ", colour = ctx.author.colour)

        couldntfinditembed = discord.Embed(title = " ", colour = ctx.author.colour)

        couldntfinditembed.add_field(name = "max amount", value = "you've got the maxiumum number of copies you can have of this item, at the moment - sorry :(")

        rocket1amount = rocket2amount = rocket3amount = rocket4amount = rocket5amount = satellite1amount = satellite2amount = satellite3amount = satellite4amount = satellite5amount = station1amount = station2amount = station3amount = station4amount = station5amount = comet1amount = comet2amount = comet3amount = comet4amount = comet5amount = planet1amount = planet2amount = planet3amount = planet4amount = planet5amount = star1amount = star2amount = star3amount = star4amount = star5amount = alien1amount = alien2amount = alien3amount = alien4amount = alien5amount = matter1amount = matter2amount = matter3amount = matter4amount = matter5amount = hole1amount = hole2amount = hole3amount = hole4amount = hole5amount = 0

        maxupgrade1 = maxupgrade2 = maxupgrade3 = maxupgrade4 = maxupgrade5 = 0

        itemwanted = item
        

        allowed_hackers = 10
        itemamount = 0
        no_more_hackers = 0
        n = 0
            
        await self.open_account(ctx.author)
        users = await self.get_bank_data()


        try:
            inventoryamountchecker = users[str(ctx.author.id)]["inv"]
        except:
            inventoryamountchecker = []

        

        for inventoryitemvaluething in inventoryamountchecker:
            inventoryitem = inventoryitemvaluething["item"]
            inventoryitemamount = inventoryitemvaluething["amount"]
        
            if inventoryitem == "rocket1":
                rocket1amount = inventoryitemamount
            elif inventoryitem == "rocket2":
                rocket2amount = inventoryitemamount
            elif inventoryitem == "rocket3":
                rocket3amount = inventoryitemamount
            elif inventoryitem == "rocket4":
                rocket4amount = inventoryitemamount
            elif inventoryitem == "rocket5":
                rocket5amount = inventoryitemamount

            elif inventoryitem == "satellite1":
                satellite1amount = inventoryitemamount
            elif inventoryitem == "satellite2":
                satellite2amount = inventoryitemamount
            elif inventoryitem == "satellite3":
                satellite3amount = inventoryitemamount
            elif inventoryitem == "satellite4":
                satellite4amount = inventoryitemamount
            elif inventoryitem == "satellite5":
                satellite5amount = inventoryitemamount

            elif inventoryitem == "station1":
                station1amount = inventoryitemamount
            elif inventoryitem == "station2":
                station2amount = inventoryitemamount
            elif inventoryitem == "station3":
                station3amount = inventoryitemamount
            elif inventoryitem == "station4":
                station4amount = inventoryitemamount
            elif inventoryitem == "station5":
                station5amount = inventoryitemamount

            elif inventoryitem == "comet1":
                comet1amount = inventoryitemamount
            elif inventoryitem == "comet2":
                comet2amount = inventoryitemamount
            elif inventoryitem == "comet3":
                comet3amount = inventoryitemamount
            elif inventoryitem == "comet4":
                comet4amount = inventoryitemamount
            elif inventoryitem == "comet5":
                comet5amount = inventoryitemamount

            elif inventoryitem == "planet1":
                planet1amount = inventoryitemamount
            elif inventoryitem == "planet2":
                planet2amount = inventoryitemamount
            elif inventoryitem == "planet3":
                planet3amount = inventoryitemamount
            elif inventoryitem == "planet4":
                planet4amount = inventoryitemamount
            elif inventoryitem == "planet5":
                planet5amount = inventoryitemamount

            elif inventoryitem == "star1":
                star1amount = inventoryitemamount
            elif inventoryitem == "star2":
                star2amount = inventoryitemamount
            elif inventoryitem == "star3":
                star3amount = inventoryitemamount
            elif inventoryitem == "star4":
                star4amount = inventoryitemamount
            elif inventoryitem == "star5":
                star5amount = inventoryitemamount

            elif inventoryitem == "alien1":
                alien1amount = inventoryitemamount
            elif inventoryitem == "alien2":
                alien2amount = inventoryitemamount
            elif inventoryitem == "alien3":
                alien3amount = inventoryitemamount
            elif inventoryitem == "alien4":
                alien4amount = inventoryitemamount
            elif inventoryitem == "alien5":
                alien5amount = inventoryitemamount
            
            elif inventoryitem == "matter1":
                matter1amount = inventoryitemamount
            elif inventoryitem == "matter2":
                matter2amount = inventoryitemamount
            elif inventoryitem == "matter3":
                matter3amount = inventoryitemamount
            elif inventoryitem == "matter4":
                matter4amount = inventoryitemamount
            elif inventoryitem == "matter5":
                matter5amount = inventoryitemamount

            elif inventoryitem == "hole1":
                hole1amount = inventoryitemamount
            elif inventoryitem == "hole2":
                hole2amount = inventoryitemamount
            elif inventoryitem == "hole3":
                hole3amount = inventoryitemamount
            elif inventoryitem == "hole4":
                hole4amount = inventoryitemamount
            elif inventoryitem == "hole5":
                hole5amount = inventoryitemamount

        if itemwanted.startswith("rocket"):
            maxupgrade1 = 1
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0
           
            if rocket1amount >= 1:
                maxupgrade1 += 1

            if rocket1amount >= 2:
                maxupgrade1 += 2
                maxupgrade2 += 1

            if rocket1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 2
                maxupgrade4 += 1

            if rocket2amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
                maxupgrade3 += 1

            if rocket2amount >= 10:
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 1

            if rocket3amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if rocket3amount >= 10:
                maxupgrade3 += 5
                maxupgrade4 += 2
          
            if rocket4amount >= 1:
                maxupgrade1 += 4
                maxupgrade2 += 3
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1

            if rocket4amount >= 10:
                maxupgrade4 += 3
            
            if rocket5amount >= 1:
                maxupgrade1 += 7
                maxupgrade2 += 3
                maxupgrade3 += 1
                maxupgrade4 += 1

            if itemwanted.endswith("1"):
                if maxupgrade1 <= rocket1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= rocket2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= rocket3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= rocket4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= rocket5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return


        if itemwanted.startswith("satellite"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if rocket5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if satellite1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if satellite1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if satellite2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if satellite2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if satellite3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if satellite3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if satellite4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if satellite5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= satellite1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= satellite2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= satellite3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= satellite4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= satellite5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
        

        if itemwanted.startswith("station"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if satellite5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if station1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if station1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if station2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if station2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if station3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if station3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if station4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if station5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= station1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= station2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= station3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= station4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= station5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            

        if itemwanted.startswith("comet"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if station5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if comet1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if comet1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if comet2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if comet2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if comet3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if comet3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if comet4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if comet5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= comet1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= comet2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= comet3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= comet4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= comet5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return

        
        if itemwanted.startswith("planet"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if comet5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if planet1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if planet1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if planet2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if planet2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if planet3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if planet3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if planet4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if planet5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= planet1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= planet2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= planet3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= planet4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= planet5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return

        
        if itemwanted.startswith("star"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if planet5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if star1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if star1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if star2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if star2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if star3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if star3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if star4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if star5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= star1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= star2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= star3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= star4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= star5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return

          
        if itemwanted.startswith("alien"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if star5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if alien1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if alien1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if alien2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if alien2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if alien3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if alien3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if alien4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if alien5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= alien1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= alien2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= alien3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= alien4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= alien5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return

        
        if itemwanted.startswith("matter"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if alien5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if matter1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if matter1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if matter2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if matter2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if matter3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if matter3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if matter4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if matter5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= matter1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= matter2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= matter3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= matter4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= matter5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return


        if itemwanted.startswith("hole"):
            maxupgrade1 = 0
            maxupgrade2 = 0
            maxupgrade3 = 0
            maxupgrade4 = 0
            maxupgrade5 = 0

            if matter5amount >= 1:
                maxupgrade1 += 1
                maxupgrade2 += 1
                maxupgrade3 += 1

            if hole1amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 1
            
            if hole1amount >= 10:
                maxupgrade1 += 5
                maxupgrade2 += 3
                maxupgrade3 += 3
                maxupgrade4 += 1
            
            if hole2amount >= 1:
                maxupgrade1 += 3
                maxupgrade2 += 1
                maxupgrade3 += 1

            if hole2amount >= 15:
                maxupgrade1 += 5
                maxupgrade2 += 3        
                maxupgrade3 += 4
                maxupgrade4 += 2        

            if hole3amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 1
                maxupgrade4 += 1
            
            if hole3amount >= 10:
                maxupgrade2 += 2
                maxupgrade4 += 3

            if hole4amount >= 1:
                maxupgrade1 += 2
                maxupgrade2 += 2
                maxupgrade3 += 2
                maxupgrade4 += 1
                maxupgrade5 += 1
            
            if hole5amount >= 1:
                maxupgrade1 += 5
                maxupgrade2 += 5
                maxupgrade3 += 3
                maxupgrade4 += 2

            if itemwanted.endswith("1"):
                if maxupgrade1 <= hole1amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("2"):
                if maxupgrade2 <= hole2amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("3"):
                if maxupgrade3 <= hole3amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("4"):
                if maxupgrade4 <= hole4amount:
                    await ctx.send(embed = couldntfinditembed)
                    return
            elif itemwanted.endswith("5"):
                if maxupgrade5 <= hole5amount:
                    await ctx.send(embed = couldntfinditembed)
                    return

        
        
        try:
            upgrades = users[str(ctx.author.id)]["upgrd"]
        except:
            upgrades = []

        for upgrd in upgrades:
            upgradename = upgrd["item"]
                

            if upgradename == "3":
                allowed_hackers += 5
            if upgradename == "4":
                allowed_hackers += 5
            if upgradename == "5":
                allowed_hackers += 5

        try:
            inv = users[str(ctx.author.id)]["inv"]
        except:
            inv = []

        if itemwanted == "hacker":
            for itemwanted in inv:
                name = itemwanted["item"]
                itemamount = itemwanted["amount"]
                    

                if name == "hacker":
                    n = itemamount

        if n >= allowed_hackers:
            await ctx.send(f"you can only have {allowed_hackers} hackers :p")
            no_more_hackers = 1
            return

        res = await self.buy_this(ctx.author,item,1,shop)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return
        
        res = await self.buy_this(ctx.author,item,1,rockets)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return

        res = await self.buy_this(ctx.author,item,1,satelites)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return

        res = await self.buy_this(ctx.author,item,1,space_stations)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return

        res = await self.buy_this(ctx.author,item,1,comets)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return

        res = await self.buy_this(ctx.author,item,1,planets)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return

        res = await self.buy_this(ctx.author,item,1,stars)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return
        
        res = await self.buy_this(ctx.author,item,1,alien_slaves)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return
        
        res = await self.buy_this(ctx.author,item,1,dark_matter)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return
        
        res = await self.buy_this(ctx.author,item,1,black_holes)
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return

        oldwallet_amount = users[str(ctx.author.id)]["wallet"]        
        newusers = await self.get_bank_data()
        wallet_amount = newusers[str(ctx.author.id)]["wallet"]

        if oldwallet_amount != wallet_amount:
            if no_more_hackers == 0:
                buyembed.add_field(name = f"️☑️ You have just bought {item}", value = f"<a:spinningspacecoin:891686810328125502> You now have {int(wallet_amount)} coins left in your wallet", inline = False)
                if item == "rocket5" and rocket5amount == 0:
                    buyembed.add_field(name = f"Congratiulations!", value = f"you just bought your first 5th tier item, you can now access the `satelites` shop")                
                
        else:
            buyembed.add_field(name = f"️❎ {item} not found", value = f"i could not find that item in any of my stores", inline = False)

        await ctx.send(embed = buyembed)

        


    @commands.command(name="upgrade", brief="upgrade some shit, indulge in capitalism")
    @cooldown(2, 5, BucketType.user)
    async def upgrade_command(self, ctx, upgrade):
        await self.open_account(ctx.author)


        res = await self.upgrade_this(ctx.author,str(upgrade),upgrades)

        if upgrade == "1":
            upgrade_name = "benjamin's recruitment"
            upgrade_icon = "<:benjaaaaaamin:890628865276395530>"
        if upgrade == "2":
            upgrade_name = "anonymous"
            upgrade_icon = "<:hacker:890644794483826688>"
        if upgrade == "3":
            upgrade_name = "benjaaaaamin's jams"
            upgrade_icon = "<:benjaaaaaaaaaaaaaaaaaaaaaaaaaaaa:890629753223143525>"
        if upgrade == "4":
            upgrade_name = "into the matrix"
            upgrade_icon = "🧑‍💻"
        if upgrade == "5":
            upgrade_name = "get intel on the FBI database"
            upgrade_icon = "<a:hackerman:890644793695293502>"


        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have enough money in your wallet to buy {upgrade_icon} {upgrade_name}")
                return
            if res[1]==3:
                await ctx.send(f"you already own {upgrade_icon} {upgrade_name}")
                return

        
        await ctx.send(f"You just upgraded {upgrade_icon} {upgrade_name}")


    @commands.command(name="sell", brief="nope")
    @cooldown(3, 10, BucketType.user)
    async def sell_command(self, ctx):
        await ctx.send("nope")


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

        totalpayout = 0
        payout = 0

        try:
            inv = bankdata[str(user.id)]["inv"]
        except:
            inv = []

        for item in inv:
            name = item["item"]
            amount = item["amount"]

            if name == "rocket2":
                payout = amount*5
                totalpayout += payout
            if name == "rocket3":
                payout = amount*20
                totalpayout += payout
            if name == "rocket4":
                payout = amount*90
                totalpayout += payout
            if name == "rocket5":
                payout = amount*500
                totalpayout += payout
            
            if name == "satellite2":
                payout = amount*400
                totalpayout += payout
            if name == "satellite3":
                payout = amount*1111
                totalpayout += payout
            if name == "satellite4":
                payout = amount*2345
                totalpayout += payout
            if name == "satellite5":
                payout = amount*5885
                totalpayout += payout
            
            if name == "station2":
                payout = amount*4554
                totalpayout += payout
            if name == "station3":
                payout = amount*12345
                totalpayout += payout
            if name == "station4":
                payout = amount*25000
                totalpayout += payout
            if name == "station5":
                payout = amount*77777
                totalpayout += payout
                
            if name == "comet2":
                payout = amount*46464
                totalpayout += payout
            if name == "comet3":
                payout = amount*123456
                totalpayout += payout
            if name == "comet4":
                payout = amount*249999
                totalpayout += payout
            if name == "comet5":
                payout = amount*626626
                totalpayout += payout

            if name == "planet2":
                payout = amount*466466
                totalpayout += payout
            if name == "planet3":
                payout = amount*1234567
                totalpayout += payout
            if name == "planet4":
                payout = amount*2469134
                totalpayout += payout
            if name == "planet5":
                payout = amount*6234567
                totalpayout += payout

            if name == "star2":
                payout = amount*4680000
                totalpayout += payout
            if name == "star3":
                payout = amount*12500000
                totalpayout += payout
            if name == "star4":
                payout = amount*25000000
                totalpayout += payout
            if name == "star5":
                payout = amount*62555555
                totalpayout += payout
            
            if name == "alien2":
                payout = amount*47474747
                totalpayout += payout
            if name == "alien3":
                payout = amount*125125125
                totalpayout += payout
            if name == "alien4":
                payout = amount*252252252
                totalpayout += payout
            if name == "alien5":
                payout = amount*629925000
                totalpayout += payout

            if name == "matter2":
                payout = amount*474474474
                totalpayout += payout
            if name == "matter3":
                payout = amount*1273888888
                totalpayout += payout
            if name == "matter4":
                payout = amount*2567000000
                totalpayout += payout
            if name == "matter5":
                payout = amount*6450000000
                totalpayout += payout

            if name == "hole2":
                payout = amount*4888888888
                totalpayout += payout
            if name == "hole3":
                payout = amount*13153000000
                totalpayout += payout
            if name == "hole4":
                payout = amount*27000000000
                totalpayout += payout
            if name == "hole5":
                payout = amount*234567654321
                totalpayout += payout
            
            else:
                pass
            
        wallet_amount = bankdata[str(user.id)]["wallet"]
        bank_amount = bankdata[str(user.id)]["bank"]

        embed = discord.Embed(title = f"", colour = ctx.author.colour, timestamp=datetime.utcnow())
        embed.add_field(name = f"{user.display_name}", value = f"placeholder", inline=False)
        embed.add_field(name = "balance", value = f"<a:spinningspacecoin:891686810328125502> {int((wallet_amount)+(bank_amount))}", inline=False)
        embed.add_field(name = "income (per hour)", value = f"<a:spinningspacecoin:891686810328125502> {totalpayout}", inline=False)

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
        bank_amount = users[str(user.id)]["bank"]

        embed = discord.Embed(title = f"{user.display_name}'s balance", colour = ctx.author.colour)
        embed.add_field(name = "wallet balance", value = f"{wallet_amount} <a:spinningspacecoin:891686810328125502>")
        embed.add_field(name = "bank balance", value = f"{bank_amount} <a:spinningspacecoin:891686810328125502>")
        await ctx.send(embed = embed)


    @commands.command(name="research", aliases=["res", "beg"], brief="researching seems to get strangers on board with your ideas, giving you money")
    @cooldown(1, 10, BucketType.user)
    async def research_command(self, ctx):
        await self.open_account(ctx.author)

        users = await self.get_bank_data()

        userid = ctx.author

        earnings = random.randrange(2, 11)

        giver = random.choice(possible_givers)

        hacker_earnings = 0
        rocket_earnings = 0
        satellite_earnings = 0
        station_earnings = 0
        comet_earnings = 0
        planet_earnings = 0
        star_earnings = 0
        alien_earnings = 0
        matter_earnings = 0
        hole_earnings = 0

      
        n = 0
        recruitment = 0

        try:
            upgrades = users[str(userid.id)]["upgrd"]
        except:
            upgrades = []

        for item in upgrades:
            name = item["item"]
            amount = item["amount"]
                

            if name == "1":
                if amount >= 1:
                    recruitment += 1
            if name == "2":
                if amount >= 1:
                    recruitment += 1
           
        try:
            inv = users[str(userid.id)]["inv"]
        except:
            inv = []

        for item in inv:
            name = item["item"]
            amount = item["amount"]
                

            if name == "hacker":
                while amount > n:
                    if recruitment == 1:
                        hacker_earning = random.choice(level2_hacker_payouts)
                    elif recruitment == 2:
                        hacker_earning = random.choice(level3_hacker_payouts)
                    else:
                        hacker_earning = random.choice(hacker_payouts)
                    hacker_earnings += hacker_earning
                    n += 1

            n = 0
            if name == "rocket1":
                while amount > n:
                    rocket_earning = random.choice(rocket1_payouts)
                    rocket_earnings += rocket_earning
                    n += 1
            n = 0
            if name == "satellite1":
                while (amount*10) > n:
                    satellite_earning = (random.choice(rocket1_payouts))*5
                    satellite_earnings += satellite_earning
                    n += 1
            n = 0
            if name == "station1":
                while (amount*9) > n:
                    station_earning = (random.choice(rocket1_payouts))*50
                    station_earnings += station_earning
                    n += 1
            n = 0
            if name == "comet1":
                while (amount*8) > n:
                    comet_earning = (random.choice(rocket1_payouts))*500
                    comet_earnings += comet_earning
                    n += 1
            n = 0
            if name == "planet1":
                while (amount*7) > n:
                    planet_earning = (random.choice(rocket1_payouts))*5000
                    planet_earnings += planet_earning
                    n += 1
            n = 0
            if name == "star1":
                while (amount*6) > n:
                    star_earning = (random.choice(rocket1_payouts))*50000
                    star_earnings += star_earning
                    n += 1
            n = 0
            if name == "alien1":
                while (amount*5) > n:
                    alien_earning = (random.choice(rocket1_payouts))*500000
                    alien_earnings += alien_earning
                    n += 1
            n = 0
            if name == "matter1":
                while (amount*4) > n:
                    matter_earning = (random.choice(rocket1_payouts))*5000000
                    matter_earnings += matter_earning
                    n += 1
            n = 0
            if name == "hole1":
                while (amount*3) > n:
                    hole_earning = (random.choice(rocket1_payouts))*50000000
                    hole_earnings += hole_earning
                    n += 1


        total_earnings = earnings + hacker_earnings + rocket_earnings + satellite_earnings + station_earnings + comet_earnings + planet_earnings + star_earnings + alien_earnings + matter_earnings + hole_earnings

        embed = discord.Embed(title = f"Research", description = f"{giver} wanted to help {ctx.author.display_name}, so they donated {earnings} <a:spinningspacecoin:891686810328125502>\n", colour = ctx.author.colour)

        
        if hole_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\nStation(s) gave you an extra {station_earnings}\nComet(s) gave you an extra {comet_earnings}\nPlanet(s) gave you an extra {planet_earnings}\nStar(s) gave you an extra {star_earnings}\nAlien(s) gave you an extra {alien_earnings}\nDark Matter gave you an extra {matter_earnings}\nBlackholes gave you an extra {hole_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif matter_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\nStation(s) gave you an extra {station_earnings}\nComet(s) gave you an extra {comet_earnings}\nPlanet(s) gave you an extra {planet_earnings}\nStar(s) gave you an extra {star_earnings}\nAlien(s) gave you an extra {alien_earnings}\nDark Matter gave you an extra {matter_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif alien_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\nStation(s) gave you an extra {station_earnings}\nComet(s) gave you an extra {comet_earnings}\nPlanet(s) gave you an extra {planet_earnings}\nStar(s) gave you an extra {star_earnings}\nAlien(s) gave you an extra {alien_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif star_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\nStation(s) gave you an extra {station_earnings}\nComet(s) gave you an extra {comet_earnings}\nPlanet(s) gave you an extra {planet_earnings}\nStar(s) gave you an extra {star_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif planet_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\nStation(s) gave you an extra {station_earnings}\nComet(s) gave you an extra {comet_earnings}\nPlanet(s) gave you an extra {planet_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif comet_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\nStation(s) gave you an extra {station_earnings}\nComet(s) gave you an extra {comet_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif station_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\nStation(s) gave you an extra {station_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif satellite_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\nSatelite(s) gave you an extra {satellite_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif hacker_earnings > 0 and rocket_earnings > 0:
            embed.add_field(name = f"\nBonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}\n\n You earnt a total of {total_earnings} <a:spinningspacecoin:891686810328125502>")
        elif rocket_earnings > 0:
            embed.add_field(name = f"Bonus earnings", value = f"Rocket(s) gave you an extra {rocket_earnings}")
        elif hacker_earnings > 0:
            embed.add_field(name = f"Bonus earnings", value = f"Hacker(s) gave you an extra {hacker_earnings}")

        users[str(userid.id)]["wallet"] += int(total_earnings)

        totalwallet = users[str(userid.id)]["wallet"]


        embed.set_footer(text = f" you now have {int(totalwallet)} coins")

        await ctx.send(embed = embed)

        with open("data/bank.json", "w") as f:
            json.dump(users, f)


    @commands.command(name="leaderboard", aliases=["lb", "top"], brief="checks the current leaderboard")
    @cooldown(2, 10, BucketType.user)
    async def leaderboard_command(self, ctx, x = 5):
        users = await self.get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
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


    @commands.command(name="withdraw", aliases=["with", "wit"], brief="puts money from your bank into your wallet")
    @cooldown(2, 10, BucketType.user)
    async def withdraw_command(self, ctx, amount = None):
        await self.open_account(ctx.author)

        if amount == None:
            await ctx.send("pleeeease enter the amount you wisd to withdraw <:shy:848650912636600320> ")
            return

        bal = await self.update_bank_data(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("you don\'t have THAT much money")
            return

        if amount < 0:
            await ctx.send("sorry, you sadly have to withdraw a positive amount of money <:smh:848652740250828821>")
            return

        await self.update_bank_data(ctx.author, amount, "wallet")
        await self.update_bank_data(ctx.author, -1*amount, "bank")

        await ctx.send(f"you withdrew {amount} <a:spinningspacecoin:891686810328125502>")



    @commands.command(name="deposit", aliases=["depo", "dep"], brief="puts money from your wallet into your bank")
    @cooldown(2, 10, BucketType.user)
    async def deposit_amount(self, ctx, amount = None):
        await self.open_account(ctx.author)

        if amount == None:
            await ctx.send("pleeeease enter the amount you wishu to deposit <:shy:848650912636600320>")
            return

        bal = await self.update_bank_data(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("you don\'t have THAT much money")
            return

        if amount < 0:
            await ctx.send("sorry, you sadly have to deposit a positive amount of money <:smh:848652740250828821>")
            return

        await self.update_bank_data(ctx.author, -1*amount, "wallet")
        await self.update_bank_data(ctx.author, amount, "bank")

        await ctx.send(f"you deposited {amount} <a:spinningspacecoin:891686810328125502>")


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

        await self.update_bank_data(ctx.author, -1*amount, "wallet")
        await self.update_bank_data(member, amount, "wallet")

        await ctx.send(f"{ctx.author.display_name} gave {amount} <a:spinningspacecoin:891686810328125502> to {member.display_name}")


    @commands.command(name="coin", aliases=["flip"], brief="flip a coin! if you win you doulbe your bet, if you lose you don\'t")
    @cooldown(1, 2, BucketType.user)
    async def coinflip(self, ctx, amount = None, side: str = "heads"):
        await self.open_account(ctx.author)

        bal = await self.update_bank_data(ctx.author)

        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to waste")
            return

        amount = int(amount)
        if amount > 50000:
            amount = 50000

        if amount > bal[0]:
            await ctx.send("you don\'t have THAT much money")
            return

        if amount < 5:
            await ctx.send("please bet at leaaaast 5 <a:spinningspacecoin:891686810328125502>")
            return
                
        if amount < 0:
            await ctx.send("sorry, you have to gamble a positive amount of money")
            return
        
        coinsides = ["heads", "tails"]
        if side not in coinsides:
            return await ctx.send("Please only use `heads` or `tails`!")

        headslist = ["heads"]

        result = random.choice(coinsides)

        msg = await ctx.send("the coin landed and...")
        await asyncio.sleep(1.5)

        if result == side:
            await self.update_bank_data(ctx.author, 1*amount, "wallet")
            
            if side in headslist:
                await msg.edit(content=f"{msg.content} it was Heads!\n{ctx.author.display_name} won {2*amount} <a:spinningspacecoin:891686810328125502>")

            else:
                await msg.edit(content=f"{msg.content} it was Tails!\n{ctx.author.display_name} won {2*amount} <a:spinningspacecoin:891686810328125502>")



        else:
            await self.update_bank_data(ctx.author, -1*amount, "wallet")

            if side in headslist:
                await msg.edit(content=f"{msg.content} it was Tails!\n{ctx.author.display_name} lost {amount} <a:spinningspacecoin:891686810328125502>")

            else:
                await msg.edit(content=f"{msg.content} it was Heads!\n{ctx.author.display_name} lost {amount} <a:spinningspacecoin:891686810328125502>")
                



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

        if amount < 5:
            await ctx.send("please bet at leaaaast 5 <a:spinningspacecoin:891686810328125502>")
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
            await ctx.send(f"{ctx.author.display_name} won {20*amount} <a:spinningspacecoin:891686810328125502>")

        elif final[0] == "<:Emerald:848602691337060412>" and final[1] == "<:Emerald:848602691337060412>" and final[2] == "<:Emerald:848602691337060412>":
            await self.update_bank_data(ctx.author, 9*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {10*amount} <a:spinningspacecoin:891686810328125502>")

        elif final[0] == "<:Gold:848602678031548427>" and final[1] == "<:Gold:848602678031548427>" and final[2] == "<:Gold:848602678031548427>":
            await self.update_bank_data(ctx.author, 13*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {14*amount} <a:spinningspacecoin:891686810328125502>")

        elif final[0] == "<:Iron:848602645207842846>" and final[1] == "<:Iron:848602645207842846>" and final[2] == "<:Iron:848602645207842846>":
            await self.update_bank_data(ctx.author, 6*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {7*amount} <a:spinningspacecoin:891686810328125502>")

        elif final[0] == "<:Redstone:848604340658241576>" and final[1] == "<:Redstone:848604340658241576>" and final[2] == "<:Redstone:848604340658241576>":
            await self.update_bank_data(ctx.author, 5*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {6*amount} <a:spinningspacecoin:891686810328125502>")

        elif final[0] == "<:Coal:848602311659618315>" and final[1] == "<:Coal:848602311659618315>" and final[2] == "<:Coal:848602311659618315>":
            await self.update_bank_data(ctx.author, 4*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {5*amount} <a:spinningspacecoin:891686810328125502>")
        
        elif final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            await self.update_bank_data(ctx.author, 0.5*amount, "wallet")
            await ctx.send(f"{ctx.author.display_name} won {1.5*amount} <a:spinningspacecoin:891686810328125502>")

        else:
            await self.update_bank_data(ctx.author, -1*amount, "wallet")
            await ctx.send(f"<:sadcat:849342846582390834> - {ctx.author.display_name} lost {amount} <a:spinningspacecoin:891686810328125502>")


    #H E L P E R     F U N C T I O N S

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
            users[str(user.id)]["bank"] = 25.0

        with open("data/bank.json", "w") as f:
            json.dump(users, f)
        
        return True

    @commands.Cog.listener()
    async def get_global_data(self):
        with open("data/bank.json", "r") as f:
            globalf = json.load(f)
        
        return globalf

    @commands.Cog.listener()
    async def add_to_global(self, change = 0):
        file = await self.get_global_data()

        file[str("GLOBAL")] += change

        with open("data/bank.json", "w") as f:
            json.dump(file, f)

        bal = [file[str("GLOBAL")]["total"]]
        return bal

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

        bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
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

        await self.update_bank_data(user,cost*-1,"wallet")

        return [True,"Worked"]

    @commands.Cog.listener()
    async def upgrade_this(self, user,upgrade_name,shop):
        upgrade_name = upgrade_name.lower()
        name_ = None
        for item in shop:
            name = item["name"].lower()
            if name == upgrade_name:
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price

        users = await self.get_bank_data()

        bal = await self.update_bank_data(user)

        if bal[0]<cost:
            return [False,2]


        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["upgrd"]:
                n = thing["item"]
                if n == upgrade_name:
                    old_amt = thing["amount"]
                    if old_amt >= 1:
                        return [False,3]
                    new_amt = old_amt + 1
                    users[str(user.id)]["upgrd"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1 
            if t == None:
                obj = {"item":upgrade_name , "amount" : 1}
                users[str(user.id)]["upgrd"].append(obj)
        except:
            obj = {"item":upgrade_name , "amount" : 1}
            users[str(user.id)]["upgrd"] = [obj]        

        with open("data/bank.json","w") as f:
            json.dump(users,f)

        await self.update_bank_data(user,cost*-1,"wallet")

        return [True,"Worked"]

def setup(bot):
    bot.add_cog(economy(bot))
