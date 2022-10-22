import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import libraries.animalLib as aniLib
from libraries.standardLib import make_4_long


class zooMisc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="zoo", brief="check your zoo")
    @cooldown(2, 10, BucketType.user)
    async def checkZoo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        await aniLib.open_zoo(self, ctx)

        userNotExist = await aniLib.check_if_zoo_not_exist(user)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        with open("storage/animals.json", "r") as f:
            zoo = json.load(f)

        data = await aniLib.get_animal_data()

        end = "s"
        if user.display_name[-1:] == "s":
            end = ""
        message_str = f"||\n||                  🌲  **{user.display_name}'{end} zoo:**  🌲\n\n"

        animalsInTiers = {
            "common": [],
            "uncommon": [],
            "rare": [],
            "epic": [],
            "mythical": [],
            "legendary": [],
        }

        caughtPerTier = {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "epic": 0,
            "mythical": 0,
            "legendary": 0,
        }

        tiers = ["common", "uncommon", "rare", "epic", "mythical", "legendary"]

        for tier in zoo:
            for i in zoo[tier]["animals"]:
                animal = zoo[tier]["animals"][i]
                icon = animal["icon"]
                name = animal["name"][0]
                caught = data[str(user.id)]["animals"][tier][name]["caught"]
                if caught != 0 or tier == "common":
                    animalsInTiers[tier].append(f"{icon}`{make_4_long(data[str(user.id)]['animals'][tier][name]['count'])}` ")

                caughtPerTier[tier] += caught

        for tier in animalsInTiers:
            if len(animalsInTiers[tier]) != 0:
                message_str += f"{zoo[tier]['icon']}    {' '.join(animalsInTiers[tier])}\n"

        print(zoo)
        message_str += "\n"
        for i, tier in enumerate(caughtPerTier):
            if caughtPerTier[tier] != 0:
                message_str += f"{caughtPerTier[tier]} {tiers[i]}, "

        message_str = message_str[:-2]

        await ctx.send(message_str)
        return

    @commands.command(
        name="dex",
        brief="check a specific animal",
    )
    @cooldown(1, 3, BucketType.user)
    async def dexCommand(self, ctx, animal: str, user: discord.Member = None):
        input = animal.lower()
        await aniLib.open_zoo(self, ctx)

        if user is None:
            user = ctx.author

        userNotExist = await aniLib.check_if_zoo_not_exist(user)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        zoo = await aniLib.get_zoo_data()
        data = await aniLib.get_animal_data()

        animalName = "none"
        for tier in zoo:
            for i in zoo[tier]["animals"]:
                animal = zoo[tier]["animals"][i]
                for nick in range(0, len(animal["name"])):
                    if input == animal["name"][nick]:
                        icon = animal["icon"]
                        animalName = animal["name"][0]
                        description = animal["description"]
                        names = ""
                        for name in animal["name"]:
                            names += f"{name}, "
                        animalTier = tier
                        break

        if animalName == "none":
            return await ctx.send(f"{input} was not found")

        if data[str(user.id)]["animals"][animalTier][animalName]["caught"] == 0:
            return await ctx.send(f"{input} was not found")

        embed = discord.Embed()
        embed.title = f"{icon} {animalName}"
        embed.color = user.colour
        embed.description = f'"{description}"'
        # embed.description = "   Can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"

        aliasesString = ""
        if len(names[(len(animalName) + 2) : -2]) >= 1:
            aliasesString = f"\n**Aliases:** {names[(len(animalName)+2):-2]}"

        embed.add_field(
            inline=False,
            name="||\n||",
            value=f"""
**Tier:** {zoo[animalTier]["icon"]} {animalTier}{aliasesString}
**Caught:** {data[str(user.id)]["animals"][animalTier][animalName]["caught"]}
**Total Caught:** {data["global"]["animals"][animalTier][animalName]["caught"]}
**Count:** {data[str(user.id)]["animals"][animalTier][animalName]["count"]}
**Sold:** {data[str(user.id)]["animals"][animalTier][animalName]["sold"]}
**Sacrificed:** {data[str(user.id)]["animals"][animalTier][animalName]["sacrificed"]}
**XP:** {data[str(user.id)]["animals"][animalTier][animalName]["xp"]}
**Coins:** {data[str(user.id)]["animals"][animalTier][animalName]["coins"]}
            """,
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(zooMisc(bot))
