import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions
import ast
import sys
import os
import glob
from yt_dlp import YoutubeDL
import asyncio

# this might be highlighted as a bug, but it's just a library written in rust lmao
# it should be fine if you've ran the setup file
#from libraries.RSmiscLib import str_replacer
from libraries.miscLib import str_replacer
from libraries.economyLib import *
from libraries.captchaLib import *


# These imports are just for the run command, for convenienceq
import subprocess
import datetime
import re
import json
import time
import requests
import random


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the or else
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.command(name="ownerdaily", brief="get your daily beaver coins here!")
    async def daily_command(self, ctx, target: discord.User):
        await open_account(self, target)

        userNotExist = await check_if_not_exist(target)
        if userNotExist == "banned":
            return
        if userNotExist:
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")

        bank = await get_bank_data()
        daily_info = bank[str(target.id)]["daily"]

        if daily_info["day"] == (datetime.utcnow() - datetime(1970, 1, 1)).days:
            return await ctx.send("they already got their daily, come back tomorrow")

        streak = ""
        if daily_info["day"] + 365 < (datetime.utcnow() - datetime(1970, 1, 1)).days - 1:
            if bank[str(target.id)]["inventory"]["insurance"] >= 1:
                await ctx.send(f"you had a streak of {daily_info['streak']}\n\nbut you own {bank[str(target.id)]['inventory']['insurance']} insurance totems\ndo you wish to spend a totem in order to mentain your streak or do you want to restart from 0?")
                await ctx.send("whoops")
                return

            else:
                streak += f"**you lost your streak of {daily_info['streak']} days :(**"
                daily_info["streak"] = 1

        else:
            daily_info["streak"] += 1
            streak += f"**{daily_info['streak']} day streak!**"
        
        
        payout = round(random.uniform(60, 120) + round(random.uniform(3.5, 6) * daily_info["streak"]))
        
        
        if payout >= 500:
            payout = 500
            
        if daily_info["streak"] > 365:
            payout += 2    
        
        # skills
        if bank[str(target.id)]["dam"]["level"] >= 4:
            payout *= 2
            streak += "\n**you got double coins for having a lvl 4+ dam**"

        # henw
        if target.id == 411536312961597440:
            payout -= 1

        payout = round(payout)

        bank[str(target.id)]["wallet"] += payout
        daily_info["day"] = (datetime.utcnow() - datetime(1970, 1, 1)).days
        bank[str(target.id)]["daily"] = daily_info

        bank[str(target.id)]["statistics"]["total_coins"] += payout

        with open("storage/playerInfo/bank.json", "w") as f:
            json.dump(bank, f)

        await ctx.send(f"you got +{payout} <:beaverCoin:1019212566095986768>!\n{streak}")

    @commands.is_owner()
    @commands.command(name="getstatus")
    async def getstatus(self, ctx):
        await ctx.send(ctx.author.activities)

    @commands.is_owner()
    @commands.command(name="nickname")
    async def change_nickname_admin(self, ctx, member: discord.Member, *, nickname=None):
        message = ctx.message
        await self.bot.http.delete_message(message.channel.id, message.id)

        if nickname == None:
            await ctx.send("please give me a nickname to change it to")
            return

        else:
            try:
                member = ctx.guild.get_member(int(member.id))
                await member.edit(nick=nickname)
                await ctx.send(
                    f"Nickname was changed to {nickname}\nbtw if anyone is wondering blame Avery for coming up with the idea for this :))))",
                    delete_after=3,
                )

            except Exception as e:
                await ctx.send(f"{e}", delete_after=5)

    @commands.is_owner()
    @commands.command(name="mepurge", brief="Clears messages equal to the amount specified ")
    @bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=0, shut="shutupplz"):
        if amount == 0:
            await ctx.send("please specifiy an amount")
            return
        if 0 < amount <= 250:
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=amount + 1):
                messages.append(message)

            await channel.delete_messages(messages)
            if shut == "shutupplz":
                await ctx.send(
                    f"{amount} messages have been purged by {ctx.message.author.mention}",
                    delete_after=10,
                )
            else:
                pass

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, extension):
        await self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} was loaded")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, extension):
        await self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} was unloaded")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        if cog == "all":
            errstr = ""
            for filename in glob.iglob("./cogs/**", recursive=True):
                if filename.endswith(".py"):  # and "owner" not in filename:
                    try:
                        filename = filename[2:].replace("/", ".")  # goes from "./cogs/economy.py" to "cogs.economy.py"
                        await self.bot.reload_extension(filename[:-3])
                        await self.bot.dispatch("load", filename[:-3])
                    except Exception as e:
                        errstr += f"{e}\n"
            if errstr == "":
                await ctx.send("All cogs were reloaded")
                return

            await ctx.send("All cogs were reloaded")
            return

        try:
            self.bot.reload_extension("cogs." + cog)
            self.bot.dispatch("load", cog)
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
            return
        await ctx.send("✅")
        print(f"------------Reloaded {cog}------------")

    @commands.is_owner()
    @commands.command(name="restart", aliases=["reboot"])
    async def restart(self, ctx):
        try:
            await self.bot.change_presence(
                status=discord.Status.idle,
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="restarting - won't respond",
                ),
            )
            await ctx.send("Restarting bot...")
            # db.commit()
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
            return

    @commands.is_owner()
    @commands.command(name="shutdown", aliases=["poweroff", "turnoff"])
    async def shutdown(self, ctx):
        try:
            await ctx.send("turning off the bot...")
            await self.bot.change_presence(
                status=discord.Status.idle,
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="turning offline - won't respond",
                ),
            )
            await self.bot.close()
            # db.commit()
            print("closed using !shutdown command")
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
            return

    @commands.is_owner()
    @commands.command(name="change_status", aliases=["setstatus", "set_status", "ownerstatus", "changestatus"])
    async def change_status_owner(self, ctx, *, input):
        try:
            await self.bot.change_presence(
                status=discord.Status.idle,
                activity=discord.Activity(type=discord.ActivityType.watching, name=f"{input}"),
            )
            await ctx.send(f"status set to ```{input}```")
        except Exception as error:
            await ctx.send(f"```py\n{error}```")

    @commands.is_owner()
    @commands.command(
        name="addtofunny",
        aliases=[
            "atf",
            "makefunny",
            "shitpostadd",
            "addshitpost",
            "jsonadd",
            "addjson",
        ],
        brief="adds the specified thing to shitpost.json",
    )
    async def addtofunnylist(ctx, *, funny=None):
        with open("./storage/shitpost.json", "r") as f:
            shitposts = json.load(f)

        if funny is None:
            print("funny is None")
            await ctx.send("funny is `None`")

        shitposts["list"].append(f"{funny}")
        await ctx.send(f"added {funny} to list")
        print(f"added {funny} to shitpost index")

        with open("./storage/shitpost.json", "w") as f:
            json.dump(shitposts, f)

    @commands.is_owner()
    @commands.command(name="ownerecho")
    async def echoownercommand(self, ctx, *, messagecontent):
        await ctx.message.delete()
        await ctx.send(messagecontent)

    @commands.is_owner()
    @commands.command(name="ecoban")
    async def ownerbaneconomy(self, ctx, user: discord.Member):
        with open("./storage/playerInfo/bank.json", "r") as f:
            data = json.load(f)

        banNr = data[str(user.id)]["anti-cheat"]["banned_x_times"]

        # 6 hours, 12 hours, 24 hours, 48 hours, so on
        bannedFor = 21600 * 2**banNr

        data[str(user.id)]["anti-cheat"]["banned_x_times"] = banNr + 1
        data[str(user.id)]["anti-cheat"]["banned_until"] = time.time() + bannedFor

        with open("./storage/playerInfo/bank.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"banned user `{user.display_name}` until <t:{time.time()+bannedFor:R}>")

    @commands.is_owner()
    @commands.command(name="pip")
    async def pipe(self, ctx, action, *, pip):
        if action == "install":
            await ctx.send(subprocess.check_call([sys.executable, "-m", "pip", f"{action}", f"{pip}"]))
        elif action == "uninstall":
            await ctx.send(subprocess.check_call([sys.executable, "-m", "pip", f"{action}", "-y", f"{pip}"]))
        else:
            await ctx.send("invalid action")
            return
        await ctx.send(f"{pip} has been {action}ed")

    @commands.command(name="repeat-embed")
    @commands.is_owner()
    async def repeatembed(self, ctx, title, desc="None", footer="None", *fields):
        embed = discord.Embed(title=title, description=desc, color=0x00FF00)
        if footer != "None":
            embed.set_footer(text=footer)
        if fields != ():
            i = 0
            while i < len(fields):
                embed.add_field(name=fields[i], value=fields[i + 1], inline=False)
                i += 2
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def run(self, ctx, *, code: str):
        """
        Run python stuff
        """
        fn_name = "_eval_expr"

        code = code.strip("` ")  # get rid of whitespace and code blocks
        if code.startswith("py\n"):
            code = code[3:]

        try:
            # add a layer of indentation
            cmd = "\n    ".join(code.splitlines())

            # wrap in async def body
            body = f"async def {fn_name}():\n    {cmd}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                "bot": self.bot,
                "ctx": ctx,
                "message": ctx.message,
                "server": ctx.message.guild,
                "channel": ctx.message.channel,
                "author": ctx.message.author,
                "commands": commands,
                "discord": discord,
                "guild": ctx.message.guild,
            }
            env.update(globals())

            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = await eval(f"{fn_name}()", env)

            out = ">>> " + code + "\n"
            output = "```py\n{}\n\n{}```".format(out, result)

            if len(output) > 2000:
                await ctx.send("The output is too long?")
            else:
                await ctx.send(output.format(result))
        except Exception as e:
            await ctx.send("```py\n>>> {}\n\n\n{}```".format(code, e))

    @commands.command(name="bash")
    @commands.is_owner()
    async def run_bash(self, ctx, *, command):
        commandArray = command.split(" ")
        await ctx.send(f"are you sure you want to run the command `{command}`?")
        try:
            response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send(f"**Timed out** cancelling")

        if response.content not in confirmations:
            return await ctx.send("oh ok")

        output = subprocess.run([*commandArray], stdout=subprocess.PIPE, timeout=180)
        output = output.stdout.decode("utf-8")

        if len(output) + len(command) < 1975:
            await ctx.send(f"`{command}` returned output:\n```{output} ```")
            return

        n = 1994
        split_strings = []

        for index in range(0, len(output), n):
            split_strings.append(output[index : index + n])

        for message in split_strings:
            await ctx.send(f"```{message}```")

    @commands.command(
        name="deletemsg",
    )
    @commands.is_owner()
    async def react_beaver_command(self, ctx, id: int = 0):

        await ctx.message.delete()
        # message = ctx.message
        # await self.bot.http.delete_message(message.channel.id, message.id)

        if ctx.message.reference:
            id = ctx.message.reference.message_id
            msg = await ctx.fetch_message(id)
            await msg.delete()

        elif id != 0:
            msg = await ctx.fetch_message(id)
            await msg.delete()

        else:
            await ctx.send(
                f"to use this command, reply to a message with {ctx.prefix}deletemsg",
                delete_after=4,
            )

    @commands.command(name="ownerreact")
    @commands.is_owner()
    async def ownerreact(self, ctx, msgid=None, emoji=None):
        try:
            message = await ctx.fetch_message(msgid)
            await message.add_reaction(emoji)
        except Exception as e:
            await ctx.send(f"Error: {e}", delete_after=20)

    @commands.command(name="download")
    @commands.is_owner()
    async def download(self, ctx, url):
        await ctx.message.delete()
        ydl_opts = {
            "format": "mp4",
            "outtmpl": "storage/videos/%(id)s.%(ext)s",
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            name = info_dict.get("id", None)
            extention = info_dict.get("ext", None)

            ydl.download(url)

        print(f"{name}.{extention} has been downloaded")
        await ctx.send(f"hi", file=discord.File(f"storage/videos/{name}.{extention}"))
        # await ctx.send(ctx.content(), file = discord.File(f"storage/videos/{url}.mp4"))

    @commands.command(name="youtube")
    @commands.is_owner()
    async def redirect_youtube(self, ctx, url):
        await ctx.message.delete()

        ydl_opts = {
            "format": "mp4",
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

        await ctx.send(info_dict["url"])

        # embed = discord.Embed(title = info_dict["title"], color = ctx.author.color, url = info_dict["url"])
        # embed.video.url = info_dict["url"]
        # print(embed.video.url)

        # await ctx.send(embed=embed)

    @commands.command(
        name="ownerremind",
    )
    @commands.is_owner()
    async def owner_remind_command(self, ctx, user: discord.Member, *, reminder):
        seconds = 0
        reminder, timing = (value for value in reminder.split(" in "))

        ch = " "
        occurrence = 2
        replacing_character = ","

        # for i in range(ceil((timing.count(ch)))):
        timing = await str_replacer(timing, ch, replacing_character, occurrence)

        timing = timing.split(",")
        for i in timing:
            if "day" in i:
                seconds += float(i.split(" ")[0]) * 86400
            elif "hour" in i:
                seconds += float(i.split(" ")[0]) * 3600
            elif "minute" in i:
                seconds += float(i.split(" ")[0]) * 60
            elif "second" in i:
                seconds += float(i.split(" ")[0])

            else:
                single_letters = i.split(" ")[1]
                if single_letters == "d":
                    seconds += float(i.split(" ")[0]) * 86400
                elif single_letters == "h" or single_letters == "hr":
                    seconds += float(i.split(" ")[0]) * 3600
                elif single_letters == "m" or single_letters == "min":
                    seconds += float(i.split(" ")[0]) * 60
                elif single_letters == "s" or single_letters == "sec":
                    seconds += float(i.split(" ")[0])

                else:
                    return await ctx.send(f"{timing} is an invalid time format, please use a valid time format - use `{ctx.prefix}help remindme` for more info")

        if seconds < 30:
            return await ctx.send(f"please set a time greater than 30 seconds")

        if seconds > 31536000:
            return await ctx.send(f"please set a time less than 1 year")

        sendtime = round(time.time() + seconds)
        embed = discord.Embed(title=reminder, description=f"i will remind {user.display_name} in <t:{sendtime}:R>", color=user.colour)
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        with open("storage/reminders.json", "r") as f:
            data = json.load(f)

        if not str(user.id) in data:
            data[str(user.id)] = {}

        data[str(user.id)][sendtime] = reminder

        with open("storage/reminders.json", "w") as f:
            json.dump(data, f)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
