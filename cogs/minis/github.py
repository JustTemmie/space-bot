import discord
from discord.ext import commands, tasks
import sys
import os
import subprocess
import glob

from git import Repo


class github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.update_git_push.start()

        self.n = 0

    @commands.command(name="update", brief="Updates the bot by pulling from github")
    @commands.is_owner()
    async def update_git_pull(self, ctx, restart="False"):
        try:
            var = subprocess.check_output(["git", "pull"])
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
            return

        output = var.decode("utf-8")

        if len(output) < 1975:
            await ctx.send(f"```{output}```")
            return

        n = 1994
        split_strings = []

        for index in range(0, len(output), n):
            split_strings.append(output[index : index + n])

        for message in split_strings:
            await ctx.send(f"```{message}```")

        if var.decode("utf-8") != "Already up to date.\n":
            if restart.lower() == "true":
                await ctx.send("Restarting...")
                await self.bot.change_presence(
                    status=discord.Status.idle,
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name="restarting - won't respond",
                    ),
                )
                os.execv(sys.executable, ["python3"] + sys.argv)
                return

            if restart.lower() == "all":
                errstr = ""
                for filename in glob.iglob("./cogs/**", recursive=True):
                    if filename.endswith(".py") and "owner" not in filename:
                        try:
                            filename = filename[2:].replace("/", ".")  # goes from "./cogs/economy.py" to "cogs.economy.py"
                            self.bot.reload_extension(filename[:-3])
                            self.bot.dispatch("load", filename[:-3])
                        except Exception as e:
                            errstr += f"{e}\n"
                if errstr == "":
                    await ctx.send("All cogs were reloaded")
                    return

                await ctx.send("All cogs were reloaded")
                return

    @commands.command(name="push", brief="Updates the bot by pushing to github")
    @commands.is_owner()
    async def update_push(self, ctx, restart=False):
        try:
            repo = Repo(".")
            repo.git.add(update=True)
            repo.index.commit("automatic commit from server to backup database")
            origin = repo.remote(name="origin")
            await ctx.send(await origin.push())
            await ctx.send("Pushed to github")
        except Exception as e:
            await ctx.send(e)

    @tasks.loop(hours=24)
    async def update_git_push(self):
        # check that N is more than 0 because this function will run on startup, and i only want it to push every 24 hours so that i don't completely clog up my github commit history
        if self.n > 0:
            try:
                repo = Repo(".")
                repo.git.add(update=True)
                repo.index.commit("automatic commit from server to backup database")
                origin = repo.remote(name="origin")
                origin.push()
            except:
                print("Some error occured while pushing the code")
        else:
            self.n += 1


async def setup(bot):
    await bot.add_cog(github(bot))
