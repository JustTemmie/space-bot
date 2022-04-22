import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions
import ast
import sys
import os
import subprocess

# These imports are just for the run command, for convenience
import datetime as dt
import re
import json


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
    @commands.command(name="mepurge", brief="Clears messages equal to the amount specified ")
    @bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount = 0, shut = "shutupplz"):
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
                await ctx.send(f'{amount} messages have been purged by {ctx.message.author.mention}', delete_after=10)
            else:
                pass

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")
          
    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} was loaded")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} was unloaded")
        
    @commands.is_owner()
    @commands.command()
    async def update(self, ctx, restart = False):
        var = subprocess.check_output(["git", "pull"])
        await ctx.send(var.decode("utf-8"))
        if var.decode("utf-8") != "Already up to date.\n" and restart != False:
            await ctx.send("Restarting...")
            os.execv(sys.executable, ['python3'] + sys.argv)
        
    
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        """
        Reloads a cog and updates changes to it
        """
        try:
            self.bot.reload_extension("cogs." + cog)
            self.bot.dispatch("load", cog)
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
            return
        await ctx.send("✅")
        print(f"------------Reloaded {cog}------------")

    @commands.is_owner()
    @commands.command(name= "restart", aliases=["reboot"])
    async def restart(self, ctx):
        try:
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="restarting - won\'t respond"))
            await ctx.send("Restarting bot...")
            os.execv(sys.executable, ['python3'] + sys.argv)
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
            return

    @commands.is_owner()
    @commands.command(name= "shutdown", aliases=["poweroff", "turnoff"])
    async def shutdown(self, ctx):
        try:
          await ctx.send("turning off the bot...")
          await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="turning offline - won\'t respond"))
          await self.bot.close()
          print("closed using !shutdown command")
        except Exception as error:
          await ctx.send(f"```py\n{error}```")
          return
    
    
    @commands.is_owner()
    @commands.command(name="addtofunny", aliases=['atf','makefunny','shitpostadd','addshitpost','jsonadd','addjson'], brief="adds the specified thing to shitpost.json")
    async def addtofunnylist(ctx, *, funny = None):
        with open("./data/shitpost.json", "r") as f:
            shitposts = json.load(f)
        
        if funny is None:
            print("funny is None")
            await ctx.send("funny is `None`")
            
        shitposts["list"].append(f"{funny}")
        await ctx.send(f"added {funny} to list")
        print(f"added {funny} to shitpost index")
        
        with open("./data/shitpost.json", "w") as f:
            json.dump(shitposts, f)


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
                'bot': self.bot,
                'ctx': ctx,
                'message': ctx.message,
                'server': ctx.message.guild,
                'channel': ctx.message.channel,
                'author': ctx.message.author,
                'commands': commands,
                'discord': discord,
                'guild': ctx.message.guild,
            }
            env.update(globals())

            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))

            out = ">>> " + code + "\n"
            output = "```py\n{}\n\n{}```".format(out, result)

            if len(output) > 2000:
                await ctx.send("The output is too long?")                    
            else:
                await ctx.send(output.format(result))
        except Exception as e:
            await ctx.send("```py\n>>> {}\n\n\n{}```".format(code, e))


def setup(bot):
    bot.add_cog(Owner(bot))
