from discord.ext import commands

import topgg
import time

from main import TOP_GG_ENCRYPTION_KEY, TOP_GG_PORT

from libraries.economyLib import *

class TopGG(commands.Cog):
    """
    This example uses dblpy's webhook system.
    In order to run the webhook, at least webhook_port must be specified (number between 1024 and 49151).
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NTIyMjYyMTc3OTg1MzMxMiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjU0MzY0MjY2fQ.tw8DM04-2TZ2EKg8DlfHDE9DvJntMKkrgRGf9NJxX00'  # set this to your DBL token
        #self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=31852)
        self.bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", TOP_GG_ENCRYPTION_KEY)
        self.bot.topgg_webhook.run(TOP_GG_PORT)  # this method can be awaited as well

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        print("Received an upvote:", "\n", data, sep="")
        
        #if data["type"] != "upvote":
        #    return
        
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
        
        data = await get_bank_data()
        
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
        
        money = random.randrange(25, 75) + (streak * random.uniform(2, 5)) + (total_votes * 2)
        logs = random.randrange(25, 75) + (streak * random.uniform(2, 5)) + (total_votes * 2)
        
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