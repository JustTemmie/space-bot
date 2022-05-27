import discord
from discord import Member, Embed
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
import json

import time


class reminderTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.reminderTask.start()
        self.cleanReminders.start()

    @tasks.loop(seconds=5)
    async def reminderTask(self):
        with open("storage/reminders.json", "r") as f:
            data = json.load(f)

        for user in data:
            for remindertime, reminderstr in zip(data[user], data[user].values()):
                if round(time.time()) >= int(remindertime):
                    userobj = await self.bot.fetch_user(user)
                    await userobj.send(f"**Reminder:** {reminderstr}")
                    data[user].pop(remindertime)
                    with open("storage/reminders.json", "w") as f:
                        json.dump(data, f)
                
                    await self.reminderTask()
                    break
    
    
    
    @tasks.loop(minutes=5)
    async def cleanReminders(self):
        with open("storage/reminders.json", "r") as f:
            data = json.load(f)

        for user in data:
            if len(data[user]) <= 0:
                data.pop(user)
                with open("storage/reminders.json", "w") as f:
                    json.dump(data, f)
                
                await self.cleanReminders()
                break
                
            
            
def setup(bot):
    bot.add_cog(reminderTask(bot))
