import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *


class ecoprofile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile", brief="tells you some basic info about the person specified")
    @cooldown(3, 10, BucketType.user)
    async def generateprofile(self, ctx, user: discord.Member = None):

        if user is None:
            await open_account(self, ctx)
            user = ctx.author

        userNotExist = await check_if_not_exist(user)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        await ctx.channel.typing()

        bankdata = await get_bank_data()

        wallet_amount = bankdata[str(user.id)]["wallet"]
        logs = bankdata[str(user.id)]["inventory"]["logs"]
        current_damlevel = bankdata[str(user.id)]["dam"]["level"]
        current_lodgelevel = bankdata[str(user.id)]["lodge"]["level"]
        current_beehivelevel = bankdata[str(user.id)]["beehive"]["level"]

        embed = discord.Embed(title=f"", colour=user.colour, timestamp=datetime.utcnow())
        embed.add_field(
            name=f"{user.display_name}",
            value=f"\"{bankdata[str(user.id)]['quote']}\"",
            inline=False,
        )
        embed.add_field(
            name="Balance:",
            value=f"<:beaverCoin:1019212566095986768> {int(wallet_amount)}\n<:log:1019212550782599220> {logs}",
            inline=False,
        )
        embed.add_field(
            name="Buildings:",
            value = f"""<:dam:1019212343760142387> Dam: LV {current_damlevel}
                        <:lodge:1019212491143786527> Lodge: LV {current_lodgelevel}
                        <:beehive:1196823754295226490> Beehive: LV {current_beehivelevel}
                        """,
            inline=False,
        )

        married_to_data = bankdata[str(user.id)]["marriage"]
        married_to = ""
        n = 0
        y = 0

        for i in married_to_data:
            i = married_to_data[i]
            if n < 10:
                if i["married"]:
                    x = await self.bot.fetch_user(i["married_to"])
                    ring = i["ring"]
                    ring_emoji = await get_ring_emoji(ring)

                    married_to += f"{ring_emoji}{x.display_name} - {datetime.utcfromtimestamp(i['time']).strftime('%Y-%m-%d %H:%M')} UTC\n"
                    n += 1

            else:
                y += 1
        if y != 0:
            married_to += f"and {y} more"

        if n == 0:
            married_to = "None"

        embed.add_field(name="Married to:", value=f"{married_to}", inline=False)

        embed.set_footer(text="Sent from my iPhone"),
        embed.set_thumbnail(url=f"{user.display_avatar.url}")

        await ctx.send(embed=embed)

    @commands.command(name="quote", brief="set a quote, make it anything you want!")
    @cooldown(5, 60, BucketType.user)
    async def set_quote(self, ctx, *, quote):
        if len(quote) > 128:
            await ctx.send("your quote is too long, please shorten it to a max of 128 characters")
            return

        await open_account(self, ctx)

        userNotExist = await check_if_not_exist(ctx.author)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        data = await get_bank_data()
        data[str(ctx.author.id)]["quote"] = quote
        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f'quote set to "{quote}"!')


async def setup(bot):
    await bot.add_cog(ecoprofile(bot))
