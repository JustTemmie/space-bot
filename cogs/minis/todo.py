from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


import libraries.standardLib as SL
from libraries.economyLib import check_if_not_exist, open_account


class todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="todo", brief="set a todo list to remember things")
    @cooldown(5, 10, BucketType.user)
    async def todoCommand(self, ctx, *, todo=None):
        if todo != None:
            if len(todo) > 125:
                await ctx.send("That todo is too long!")
                return

        if await check_if_not_exist(ctx.author):
            await open_account(self, ctx)

            if await check_if_not_exist(ctx.author):
                return

        with open("storage/todo.json", "r") as f:
            data = json.load(f)

        if str(ctx.author.id) not in data:
            data[str(ctx.author.id)] = []

        if todo != None:
            if len(data[str(ctx.author.id)]) > 15:
                await ctx.send(f"you have too many todos, please delete some using {ctx.prefix}delete todo <number>")
                return
            data[str(ctx.author.id)].append(todo)

            with open("storage/todo.json", "w") as f:
                json.dump(data, f)

            await ctx.send(f"{ctx.author.mention} your todo has been added to the list with index {len(data[str(ctx.author.id)])}\n```{todo}```")
            return

        end = ""
        if ctx.author.display_name[-1:] != "s":
            end = "s"
        embed = Embed(title=f"{ctx.author.display_name}'{end} Todo List", description="", color=ctx.author.color)
        embed.set_footer(text=f"use {ctx.prefix}delete todo <index> to delete a todo")

        for i, reminder in enumerate(data[str(ctx.author.id)]):
            embed.add_field(name=f"{i+1}", value=reminder, inline=False)

        try:
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(
                f"{ctx.author.mention} your todo list is too long to be displayed in a embed, please use {ctx.prefix}delete todo <index> to delete a todo"
            )

    @commands.command(name="delete", brief="delete a todo from your todo list")
    @cooldown(5, 10, BucketType.user)
    async def deleteTodo(self, ctx, todo, index):
        if todo != "todo":
            await ctx.send(f"as of now, you need to use `todo` as the first argument\n`{ctx.prefix}delete todo <index>`")
            return

        if await check_if_not_exist(ctx.author):
            await open_account(self, ctx)

            if await check_if_not_exist(ctx.author):
                return

        with open("storage/todo.json", "r") as f:
            data = json.load(f)

        if str(ctx.author.id) not in data:
            await ctx.send("you have no todos")
            return

        try:
            old_todo = data[str(ctx.author.id)][(int(index) - 1)]
            data[str(ctx.author.id)].pop(int(index) - 1)
            await ctx.send(f"todo nr {index} has been deleted\n```{old_todo}```")
            with open("storage/todo.json", "w") as f:
                json.dump(data, f)

        except Exception as e:
            await ctx.send(f"error: {e}")


async def setup(bot):
    await bot.add_cog(todo(bot))
