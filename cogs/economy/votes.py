from discord.ext import commands

import topgg
import time

from main import TOP_GG_ENCRYPTION_KEY, TOP_GG_PORT, TOP_GG_TOKEN

from libraries.economyLib import *
from libraries.settings import *

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
        
        if time.time() < 1654497044: # placeholder
            weekendstr = "\nit's the weekend, you got double rewards!"
            is_weekend = True
        
        try:  # needs testing when it's not a weekend lmao
            if data["is_weekend"]:
                print("weekend vote!")
        except:
            pass

        user = int(data['user'])
        
        userObj = self.bot.get_user(user)
        
        await open_account(userObj)
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
        if time.time() - data[str(user)]["dailyvote"]["last_vote"] >= 172800: # 48 hours
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
        
        money = random.randrange(25, 75) + (streak * random.uniform(2, 4)) + (total_votes * 1.5)
        logs = random.randrange(25, 75) + (streak * random.uniform(2, 4)) + (total_votes * 1.5)
        
        logs *= 0.6
        
        if is_weekend:
            money *= 2
            logs *= 2


        money = int(round(money, 0))
        logs = int(round(logs, 0))

        try:
            await userObj.send(f"You have received **{money}** <:beaverCoin:968588341291397151> and **{logs}** <:log:970325254461329438> for voting!{streakstr}{weekendstr}")
            sucessstr = f"Successfully sent a vote confirmation to {userObj.name}!"
        except Exception as e:
            sucessstr = f"Failed to send a vote confirmation to {userObj.name}!\n{e}"

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


def setup(bot):
    bot.add_cog(TopGG(bot))