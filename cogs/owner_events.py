import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions
import ast
import sys
import os
import subprocess

class owner_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def pushToGit():
        currDir = os.path.dirname(os.path.realpath(sys.argv[0]))
        try:
            shutil.rmtree(os.path.join(currDir, '.git'))
        except:
            pass
        try:
            cp = cmd.run("git init", check=True, shell=True, cwd=currDir)
            cp = cmd.run(f"git remote add origin git@github.com:johnsmith/repo_hold.git", check=True, shell=True, cwd=currDir + "//")
            cp = cmd.run("git config user.name 'john smith'", check=True, shell=True, cwd=currDir + "//")
            cp = cmd.run("git config user.email 'john@smith.com'", check=True, shell=True, cwd=currDir + "//")
            cp = cmd.run("git add .", check=True, shell=True, cwd=currDir + "//")
            message = f"Some generated message here"
            cp = cmd.run(f"git commit -m '{message}'", check=True, shell=True, cwd=currDir + "//")
            cp = cmd.run("git push -u origin master", check=True, shell=True, cwd=currDir + "//")
            return True
        except Exception as e:
            return False


def setup(bot):
    bot.add_cog(Owner(bot))