import discord
from discord.ext import commands, tasks
from discord.errors import Forbidden
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown
from datetime import datetime

import logging
import json
import os

from time import time
from math import floor

cooldown_dictionary = {}

IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_timer.start()
        #self.genshin_nick.start()
        self.send_hourly_log.start()

    @commands.Cog.listener()
    async def on_error(self, err, *args, **kwargs):
        await self.bot.get_channel(984577196616216616).send(f"{err}")
        
        if err == "on_command_error":
            await args[0].send("Sorry, something unexpected went wrong.")
            # raise

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            # await ctx.send("Sorry, I couldn't find that command")
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(
                f"One or more of the required arguments are missing, perhaps the help command could help you out? `{ctx.prefix}help {ctx.command}`"
            )

        elif isinstance(exc, CommandOnCooldown):

            
            ####################
            # this section makes it so the bot will only respond with "that command is on cooldown" a max of 3 times every 10 seconds for each user
            if ctx.author.id not in cooldown_dictionary:
                cooldown_dictionary[ctx.author.id] = {}
                cooldown_dictionary[ctx.author.id][0] = time()
            
            for i in range(0, len(cooldown_dictionary[ctx.author.id])):
                if cooldown_dictionary[ctx.author.id][i]+10 < time():
                    cooldown_dictionary[ctx.author.id][i] = time()
                    break
                
                if i == len(cooldown_dictionary[ctx.author.id])-1:
                    cooldown_dictionary[ctx.author.id][i+1] = time()
                
                if i == 2:
                    return
            ####################
            
            await ctx.send(
                f"That command is on cooldown. Please try again in {exc.retry_after:,.2f} seconds.",
                delete_after=(exc.retry_after*1.05 + 0.7),
            )

        #      elif isinstance(exc.original, HTTPException):
        #          await ctx.send("Unable to send message.")

        elif hasattr(exc, "original"):
            # raise exc  # .original

            if isinstance(exc.original, Forbidden):
                await ctx.send(f"I do not have the permission to do that\n{exc}")

            else:
                await ctx.send(exc.original)
                raise exc.original

        else:
            await ctx.send(exc)
            raise exc

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        logging.info(f"{ctx.command.name} was successfully invoked by {ctx.author}")
        print(f"{ctx.command.name} was successfully invoked by {ctx.author} {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
        fileObj = open(f'temp/hourlyLogs/{floor(time()/3600)}.txt', 'a')
        fileObj.write(f"{ctx.command.name} was successfully invoked by {ctx.author} at {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}\n")
        fileObj.close()


    @commands.Cog.listener()
    async def on_message(self, ctx):
        with open("tof-project/everyone.json", "r") as f:
                file = json.load(f)

        file[str(time())] = ctx

        with open("tof-project/everyone.json", "w") as f:
            json.dump(file, f)

    @tasks.loop(seconds=10)
    async def update_timer(self):
        if self.bot.is_ready():
            with open("storage/misc/time.json", "w") as f:
                json.dump((datetime.utcnow() - datetime(1970, 1, 1)).seconds, f)
            
    
    @tasks.loop(seconds=30)
    async def send_hourly_log(self):
        if self.bot.is_ready():
            for file in os.listdir("temp/hourlyLogs"):
                if file != f"{floor(time() / 3600)}.txt":
                    await self.bot.get_channel(978695336048623713).send(file=discord.File(f"temp/hourlyLogs/{file}"))
                    os.remove(f"temp/hourlyLogs/{file}")




async def setup(bot):
    await bot.add_cog(events(bot))
