import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot_has_permissions
import ast
import sys
import os
import subprocess

from git import Repo


class github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.update_git_push.start()

        self.n = 0

    @commands.command(name="update", brief="Updates the bot by pulling from github")
    @commands.is_owner()
    async def update_git_pull(self, ctx, restart=False):
        var = subprocess.check_output(["git", "pull"])
        await ctx.send(var.decode("utf-8"))
        if var.decode("utf-8") != "Already up to date.\n" and restart != False:
            await ctx.send("Restarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

    @commands.command(name="push", brief="Updates the bot by pushing to github")
    @commands.is_owner()
    async def update_push(self, ctx, restart=False):
        try:
            repo = Repo(".")
            repo.git.add(update=True)
            repo.index.commit("automatic commit from server to backup database")
            origin = repo.remote(name="origin")
            await ctx.send(origin.push())
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


def setup(bot):
    bot.add_cog(github(bot))
