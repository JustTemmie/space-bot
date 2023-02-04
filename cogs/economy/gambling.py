from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import asyncio


from libraries.economyLib import *
import libraries.standardLib as SL


class ecogambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="coinflip",
        aliases=["flip", "cf"],
        brief="flip a coin! if you win you double your bet, if you lose you don't",
    )
    @cooldown(1, 2, BucketType.user)
    async def coinflip(self, ctx, amount=None, side: str = "heads"):
        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to waste")
            return

        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        bal = await update_bank_data(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount > 100000:
            amount = 100000

        if amount < 5:
            await ctx.send("please bet at leaaaast 5 <:beaverCoin:1019212566095986768>")
            return

        if amount > bal[0]:
            await ctx.send("you don't have THAT much money")
            return

        coinsides = ["Heads", "Tails"]

        result = coinsides[random.randint(0, 1)]
        msg = await ctx.reply("the coin was tossed into the air and...")
        await asyncio.sleep(1.0)

        bal = await update_bank_data(ctx.author)
        if amount > bal[0]:
            await msg.edit(content=f"{msg.content} it... didn't land??!\n{ctx.author.display_name} won {amount} <:beaverCoin:1019212566095986768>")
            return

        if result.lower() == side.lower():
            await update_bank_data(ctx.author, amount, "wallet")
            await msg.edit(content=f"{msg.content} it landed on {result}!\n{ctx.author.display_name} won {2*amount} <:beaverCoin:1019212566095986768>")
            return

        await update_bank_data(ctx.author, -amount, "wallet")
        await msg.edit(content=f"{msg.content} it landed on {result}!\n{ctx.author.display_name} lost {amount} <:beaverCoin:1019212566095986768>")

    @commands.command(
        name="slot",
        aliases=["slots"],
        brief="do you ever wish you didn't have any money? introducing, gambling™",
    )
    @cooldown(1, 5, BucketType.user)
    async def slot_machine_command(self, ctx, amount=None):

        ##########################################################################
        ########## THIS CODE IS TERRIBLE AND NO I'M NOT FIXING IT SORRY ##########
        ##########################################################################
        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        if amount == None:
            await ctx.send("pleeeease enter the amount you wish to waste")
            return

        bal = await update_bank_data(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(float(amount))
        if amount > 50000:
            amount = 50000

        if amount > bal[0]:
            await ctx.send("you don't have THAT much money")
            return

        if amount < 3:
            await ctx.send("please bet at leaaaast 3 <:beaverCoin:1019212566095986768>")
            return

        final = []

        slot1 = "<a:slots:849627985857871912>"
        slot2 = "<a:slots:849627985857871912>"
        slot3 = "<a:slots:849627985857871912>"

        msg = await ctx.send(str(final)[:-2] + (str(slot1)) + (str(slot2)) + (str(slot3)))
        await asyncio.sleep(2)

        slot1 = random.choice(
            [
                "<:Coal:848602311659618315>",
                "<:Redstone:848604340658241576>",
                "<:Iron:848602645207842846>",
                "<:Gold:848602678031548427>",
                "<:Emerald:848602691337060412>",
                "<:Diamond:848602702132019210>",
            ]
        )
        final.append(slot1)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")
        await asyncio.sleep(1.5)

        slot2 = random.choice(
            [
                "<:Coal:848602311659618315>",
                "<:Redstone:848604340658241576>",
                "<:Iron:848602645207842846>",
                "<:Gold:848602678031548427>",
                "<:Emerald:848602691337060412>",
                "<:Diamond:848602702132019210>",
            ]
        )
        final.append(slot2)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")
        await asyncio.sleep(1.5)

        slot3 = random.choice(
            [
                "<:Coal:848602311659618315>",
                "<:Redstone:848604340658241576>",
                "<:Iron:848602645207842846>",
                "<:Gold:848602678031548427>",
                "<:Emerald:848602691337060412>",
                "<:Diamond:848602702132019210>",
            ]
        )
        final.append(slot3)
        await msg.edit(content=f"{str(slot1)}{str(slot2)}{str(slot3)}")

        bal = await update_bank_data(ctx.author)
        if amount > bal[0]:
            await msg.reply("nice try ||beaver||")
            return

        if final[0] == "<:Diamond:848602702132019210>" and final[1] == "<:Diamond:848602702132019210>" and final[2] == "<:Diamond:848602702132019210>":
            await update_bank_data(ctx.author, 19 * amount, "wallet")
            await msg.reply(f"{await SL.removeat(ctx.author.display_name)} won {20*amount} <:beaverCoin:1019212566095986768>")

        elif final[0] == "<:Emerald:848602691337060412>" and final[1] == "<:Emerald:848602691337060412>" and final[2] == "<:Emerald:848602691337060412>":
            await update_bank_data(ctx.author, 9 * amount, "wallet")
            await msg.reply(f"{await SL.removeat(ctx.author.display_name)} won {10*amount} <:beaverCoin:1019212566095986768>")

        elif final[0] == "<:Gold:848602678031548427>" and final[1] == "<:Gold:848602678031548427>" and final[2] == "<:Gold:848602678031548427>":
            await update_bank_data(ctx.author, 13 * amount, "wallet")
            await msg.reply(f"{await SL.removeat(ctx.author.display_name)} won {14*amount} <:beaverCoin:1019212566095986768>")

        elif final[0] == "<:Iron:848602645207842846>" and final[1] == "<:Iron:848602645207842846>" and final[2] == "<:Iron:848602645207842846>":
            await update_bank_data(ctx.author, 6 * amount, "wallet")
            await msg.reply(f"{await SL.removeat(ctx.author.display_name)} won {7*amount} <:beaverCoin:1019212566095986768>")

        elif final[0] == "<:Redstone:848604340658241576>" and final[1] == "<:Redstone:848604340658241576>" and final[2] == "<:Redstone:848604340658241576>":
            await update_bank_data(ctx.author, 5 * amount, "wallet")
            await msg.reply(f"{await SL.removeat(ctx.author.display_name)} won {6*amount} <:beaverCoin:1019212566095986768>")

        elif final[0] == "<:Coal:848602311659618315>" and final[1] == "<:Coal:848602311659618315>" and final[2] == "<:Coal:848602311659618315>":
            await update_bank_data(ctx.author, 4 * amount, "wallet")
            await msg.reply(f"{await SL.removeat(ctx.author.display_name)} won {5*amount} <:beaverCoin:1019212566095986768>")

        elif final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            await update_bank_data(ctx.author, 0.5 * amount, "wallet")
            await msg.reply(f"{await SL.removeat(ctx.author.display_name)} won {1.5*amount} <:beaverCoin:1019212566095986768>")

        else:
            await update_bank_data(ctx.author, -1 * amount, "wallet")
            await msg.reply(f"<:sadcat:849342846582390834> - {await SL.removeat(ctx.author.display_name)} lost {amount} <:beaverCoin:1019212566095986768>")



    @commands.command(
        name="blackjack",
        aliases=["bj"],
        description="gamble with cards!"
    )
    async def blackjack(self, ctx, amount=1):
        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        bal = await update_bank_data(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(float(amount))
        if amount > 50000:
            amount = 50000

        if amount > bal[0]:
            await ctx.send("you don't have THAT much money")
            return

        await update_bank_data(ctx.author, -amount, "wallet")
    
        player_hand = []
        dealer_hand = []

        # Deal the initial cards
        player_hand.append(self.get_random_card())
        player_hand.append(self.get_random_card())
        dealer_hand.append(self.get_random_card())
        dealer_hand.append(self.get_random_card())

        # Calculate the initial scores
        player_score = self.get_hand_value(player_hand)
        dealer_score = self.get_hand_value(dealer_hand[0])
        
        embed = self.render_message(ctx, player_hand, dealer_hand)
        
        embedMessage = await ctx.send(embed=embed)
        
        if player_score == 21:
            if self.get_hand_value(dealer_hand) == 21:
                embed = self.render_message(ctx, player_hand, dealer_hand, True, embed)
                embed.description = "Both got blackjacks, it's a tie!"
                await embedMessage.edit(embed=embed)
                await update_bank_data(ctx.author, amount, "wallet")
                return

            embed = self.render_message(ctx, player_hand, dealer_hand, True, embed)
            embed.description = f"Woah! Blackjack, you won {amount*3} <:beaverCoin:1019212566095986768>!"
            await embedMessage.edit(embed=embed)
            await update_bank_data(ctx.author, amount*3, "wallet")
            

        # Player turn
        while player_score < 21:
            if len(player_hand) != 2:
                embed = self.render_message(ctx, player_hand, dealer_hand, False, embed)
                await embedMessage.edit(embed=embed)

            # Wait for player's response, only accepting hit and stand
            def check(m):
                return m.author == ctx.author and m.content.lower() in ["hit", "stand"]
            try:
                response = await self.bot.wait_for("message", check=check, timeout = 180)
            except asyncio.TimeoutError:
                return await ctx.send(f"**Timed out** {SL.removeat(ctx.author.display_name)} took too long to chose, you lose")

            if response.content.lower() == "hit":
                player_hand.append(self.get_random_card())
                player_score = self.get_hand_value(player_hand)
                if player_score > 21:
                    embed = self.render_message(ctx, player_hand, dealer_hand, False, embed)
                    embed.description = "You bust! Better luck next time"
                    await embedMessage.edit(embed=embed)
                    return
            else:
                break

        # Dealer turn
        while dealer_score < 17:
            dealer_hand.append(self.get_random_card())
            dealer_score = self.get_hand_value(dealer_hand)
            if dealer_score > 21:
                embed = self.render_message(ctx, player_hand, dealer_hand, True, embed)
                embed.description = f"Dealer busts! You win {2*amount} <:beaverCoin:1019212566095986768>!"
                await embedMessage.edit(embed=embed)
                await update_bank_data(ctx.author, 2*amount, "wallet")
                return

        # Compare scores
        if player_score > dealer_score:
            await update_bank_data(ctx.author, 2*amount, "wallet")
            embed = self.render_message(ctx, player_hand, dealer_hand, True, embed)
            embed.description = f"You win {2*amount} <:beaverCoin:1019212566095986768>!"
            await embedMessage.edit(embed=embed)
        elif player_score <= dealer_score:
            embed = self.render_message(ctx, player_hand, dealer_hand, True, embed)
            embed.description = "You lose. Better luck next time"
            await embedMessage.edit(embed=embed)
        else:
            await update_bank_data(ctx.author, amount, "wallet")
            embed = self.render_message(ctx, player_hand, dealer_hand, True, embed)
            embed.description = f"error occured: this should be unreachable"
            await embedMessage.edit(embed=embed)

    def get_random_card(self):
        return random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])

    def get_hand_value(self, hand):
        value = 0
        for card in hand:
            if card == "J" or card == "Q" or card == "K":
                value += 10
            elif card == "A":
                value += 11
            else:
                value += int(card)

        for card in hand:
            if value > 21 and card == "A":
                value -= 10

        return value
    
    def render_message(self, ctx, player_hand, dealer_hand, reveal_dealer = False, embed = None):
        if embed == None:
            embed = Embed(title="Blackjack!")
            embed.colour = ctx.author.colour
        
        embed.clear_fields()
        
        embed.add_field(name="Your Hand", value=f"{', '.join(player_hand)} (total: {self.get_hand_value(player_hand)})", inline=False)
        
        if reveal_dealer:
            embed.add_field(name="Dealer's Hand", value=f"{', '.join(dealer_hand)} (total: {self.get_hand_value(dealer_hand)})", inline=False)
        else:
            embed.add_field(name="Dealer's face-up card", value=f"{dealer_hand[0]} (total: {self.get_hand_value(dealer_hand[0])})", inline=False)
        
        return embed


async def setup(bot):
    await bot.add_cog(ecogambling(bot))
