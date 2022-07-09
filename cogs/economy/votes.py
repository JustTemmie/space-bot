from discord.ext import commands

import topgg
import time

from libraries.economyLib import *
from libraries.settings import *

from os import getenv
from dotenv import load_dotenv

load_dotenv("keys.env")
TOP_GG_TOKEN = getenv("TOP_GG_TOKEN")
TOP_GG_PORT = getenv("TOP_GG_PORT")
TOP_GG_ENCRYPTION_KEY = getenv("TOP_GG_ENCRYPTION_KEY")

class TopGG(commands.Cog):
    """
    This example uses dblpy's webhook system.
    In order to run the webhook, at least webhook_port must be specified (number between 1024 and 49151).
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = TOP_GG_TOKEN # set this to your DBL token
        #self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=31852)
        self.bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", TOP_GG_ENCRYPTION_KEY)
        self.bot.topgg_webhook.run(TOP_GG_PORT)  # this method can be awaited as well

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        #print("Received an upvote:", "\n", data, sep="")
        
        
        weekendstr = ""
        streakstr = ""
        is_weekend = False
        
        print(data)

        try:
            if data["is_weekend"]:
                is_weekend = True
                weekendstr = "\nit's the weekend, you got double rewards!"
        except Exception as e:
            print(f"VOTE ERROR {e}")
            await self.bot.get_channel(978695336283480146).send(f"VOTE ERROR {e}\nData: {data}")
            
        user = int(data['user'])
        
        userObj = self.bot.get_user(user)
        
        if await check_if_not_exist(userObj):
            return await userObj.send("sorry, you need to create an account before getting vote rewards :/")
        
        await store_settings(userObj)
        
        data = await get_bank_data()
        settings = await get_user_settings()
        
        if settings[str(user)]["vote"]["reminder"]:
            with open("storage/reminders.json", "r") as f:
                reminderData = json.load(f)
            
            if not str(user) in reminderData:
                reminderData[str(user)] = {}
            
            reminderData[str(user)][int(round(time.time())) + 43230] = "you can now vote again!\nhttps://top.gg/bot/765222621779853312/vote\nif you want to disable reminders do `a!set vote reminder false`"
            
            with open("storage/reminders.json", "w") as f:
                json.dump(reminderData, f)
        
        
        # if data["type"] != "upvote":
        #     money = logs = 0
        
        # else:
        if time.time() - data[str(user)]["dailyvote"]["last_vote"] >= 259200: # 72 hours
            if data[str(user)]["dailyvote"]["streak"] != 0:
                streakstr = f"\nYou lost your streak of **{data[str(user)]['dailyvote']['streak']}** votes :("
            
            data[str(user)]["dailyvote"]["streak"] = 0
        
        else:
            data[str(user)]["dailyvote"]["streak"] += 1
            streakstr = f"\nYou have a streak of **{data[str(user)]['dailyvote']['streak']}** votes!"
        
        data[str(user)]["dailyvote"]["last_vote"] = time.time()
        data[str(user)]["dailyvote"]["total_votes"] += 1
        
        streak = data[str(user)]["dailyvote"]["streak"]
        total_votes = data[str(user)]["dailyvote"]["total_votes"]
        
        money = random.randrange(25, 75) + (streak * random.uniform(0.2, 0.5)) + (total_votes * 0.3)
        logs = random.randrange(25, 75) + (streak * random.uniform(0.2, 0.5)) + (total_votes * 0.3)
        
        logs *= 0.6
        
        if is_weekend:
            money *= 2
            logs *= 2


        money = int(round(money, 0))
        logs = int(round(logs, 0))

        try:
            await userObj.send(f"You have received **{money}** <:beaverCoin:968588341291397151> and **{logs}** <:log:970325254461329438> for voting!{streakstr}{weekendstr}")
            sucessstr = f"Successfully sent a vote confirmation to {userObj.name}!\nData: {data}"
        except Exception as e:
            sucessstr = f"Failed to send a vote confirmation to {userObj.name}!\nData: {data}"
            print(f"VOTE ERROR {e}")

        data[str(user)]["wallet"] += money
        data[str(user)]["inventory"]["logs"] += logs

        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)
        
        await self.bot.get_channel(982955577007292427).send(sucessstr)



    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        return
        print("Received a test upvote:", "\n", data, sep="")
       #print(int(data['user']) + 10)


async def setup(bot):
    await bot.add_cog(TopGG(bot))