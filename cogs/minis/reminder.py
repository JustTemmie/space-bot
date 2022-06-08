import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

from math import ceil
from datetime import datetime
import time

#from libraries.miscLib import str_replacer
from libraries.RSmiscLib import str_replacer
# this might be highlighted as a bug, but it's just a library written in rust lmao
# it should be fine if you've ran the setup file

import libraries.standardLib as SL 

class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name="remindme",
        aliases = ["remind", "reminder"],
        brief="reminds you of something\na!remindme god damn it tell her i like beavers in 1 day 2 hours 30 min\nyou can use \"day(s), d\", \"hour(s), h(r)\", \"minute(s), m(in)\", \"second(s), s(ec)\"",
        )
    @cooldown(5, 10, BucketType.user)
    async def reminder_command(self, ctx, *, reminder):
        seconds = 0
        reminder, timing = (value for value in reminder.split(" in "))
        
        ch = " "
        occurrence = 2
        replacing_character = ','
        

        #for i in range(ceil((timing.count(ch)))):
        timing = str_replacer(timing, ch,
            replacing_character, occurrence)
        
        timing = timing.split(",")
        for i in timing:
            if "day" in i:
                seconds += int(i.split(" ")[0]) * 86400
            elif "hour" in i:
                seconds += int(i.split(" ")[0]) * 3600
            elif "minute" in i:
                seconds += int(i.split(" ")[0]) * 60
            elif "second" in i:
                seconds += int(i.split(" ")[0])
            
            
            else:
                single_letters = (i.split(" ")[1])
                if single_letters == "d":
                    seconds += int(i.split(" ")[0]) * 86400
                elif single_letters == "h" or single_letters == "hr":
                    seconds += int(i.split(" ")[0]) * 3600
                elif single_letters == "m" or single_letters == "min":
                    seconds += int(i.split(" ")[0]) * 60
                elif single_letters == "s" or single_letters == "sec":
                    seconds += int(i.split(" ")[0])
                
                else:
                    return await ctx.send(f"{timing} is an invalid time format, please use a valid time format - use `{ctx.prefix}help remindme` for more info")

        
        if seconds < 30:
            return await ctx.send(f"please set a time greater than 30 seconds")
        
        if seconds > 31536000:
            return await ctx.send(f"please set a time less than 1 year")
        

        sendtime = round(time.time() + seconds)
        embed = Embed(title=reminder, description = f"i will remind you <t:{sendtime}:R>", color=ctx.author.colour)
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
        
        with open("storage/reminders.json", "r") as f:
            data = json.load(f)
        
        
        if not str(ctx.author.id) in data:
            data[str(ctx.author.id)] = {}
        
        data[str(ctx.author.id)][sendtime] = reminder
        
        with open("storage/reminders.json", "w") as f:
            json.dump(data, f)
        
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(reminder(bot))
