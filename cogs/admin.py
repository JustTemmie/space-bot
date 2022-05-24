from ast import alias
import discord
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import (
    Cog,
    Greedy,
    CheckFailure,
    command,
    has_permissions,
    bot_has_permissions,
)
import json
import asyncio

from libraries.miscLib import get_input

class admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="kick", brief="Kicks the specified users")
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def kick_members(
        self,
        ctx,
        targets: Greedy[Member],
        *,
        reason: Optional[str] = "No reason provided",
    ):
        if not len(targets):
            await ctx.send("One or more of the required arguments are missing")

        else:
            for target in targets:
                await target.kick(reason=reason)
                embed = Embed(title="Member kicked", colour=0xDD2222, timestamp=datetime.utcnow())

                fields = [
                    ("Member", f"{target.mention} a.k.a. {target.display_name}", False),
                    ("Actioned by", ctx.author.mention, False),
                    ("ID", target.id, False),
                    ("Name", str(target), False),
                    (
                        "Created at in UTC",
                        target.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                        True,
                    ),
                    (
                        "Joined at in UTC",
                        target.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
                        True,
                    ),
                    ("Top role", target.top_role.mention, False),
                    ("Reason", reason, False),
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                embed.set_thumbnail(url=target.avatar_url)
                await self.bot.get_channel(772591539423281172).send(embed=embed)
                await ctx.send(embed=embed)

    @kick_members.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform that task")

    @command(name="warn", brief="Warns the specified users")
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def warn_members(
        self,
        ctx,
        targets: Greedy[Member],
        *,
        reason: Optional[str] = "No reason provided",
    ):
        rule_breakers_id = []
        rule_breakers = ""
        for user in targets:
            rule_breakers_id.append(user.id)
            rule_breakers.append(user.name + ", ")

        embed = discord.Embed(title="Warning issued: ", color=0xF40000)
        embed.add_field(name="Warning: ", value=f"Reason: {reason}", inline=False)
        embed.add_field(name="User(s) warned: ", value=f"{rule_breakers}", inline=False)
        embed.add_field(name="Warned by: ", value=f"{ctx.author}", inline=False)

        await ctx.send(embed=embed)


    @command(name="ban", brief="Bans the specified users")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(
        self,
        ctx,
        targets: Greedy[Member],
        *,
        reason: Optional[str] = "No reason provided",
    ):
        if not len(targets):
            await ctx.send("One or more of the required arguments are missing")

        else:
            for target in targets:
                await target.ban(reason=reason)

                embed = Embed(title="Member banned", colour=0xDD2222, timestamp=datetime.utcnow())

                fields = [
                    ("Member", f"{target.mention} a.k.a. {target.display_name}", False),
                    ("Actioned by", ctx.author.mention, False),
                    ("ID", target.id, False),
                    ("Name", str(target), False),
                    (
                        "Created at in UTC",
                        target.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                        True,
                    ),
                    (
                        "Joined at in UTC",
                        target.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
                        True,
                    ),
                    ("Top role", target.top_role.mention, False),
                    ("Reason", reason, False),
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

            embed.set_thumbnail(url=target.avatar_url)
            await self.bot.get_channel(772591539423281172).send(embed=embed)
            await ctx.send(embed=embed)

    @ban_members.error
    async def ban_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform that task")

    
    @commands.command(
        name="rolemenu",
        aliases=["role", "rolelist", "role-menu"],
        brief="Setup a role menu to give users roles by reacting to emojis",
    )
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def rolemenu(self, ctx):
        await ctx.send("This command is currently under development")
        guild = ctx.guild

        roles = 0
        max_roles = 30
        
        await ctx.send("What should the name of the role menu/embed be?")
        response = await get_input(self, ctx)
        embed = discord.Embed(title = response.content, color = 0x00FF00)
        msg = await ctx.send(embed = embed)
        
        await ctx.send("What should the description of the role menu/embed be? if you don't want one, just type 'none'")
        response = await get_input(self, ctx)
        if not response.content.lower() in ["none", "n", "no"]:
            embed.description = response.content
        await msg.edit(embed = embed)
        
        try:
            with open(f"storage/reactions/roles/{ctx.channel.id}.json", "r") as f:
                data = json.load(f)
        except:
            with open(f"storage/reactions/roles/{ctx.channel.id}.json", "w") as f:
                data = []
        
        for i in range(max_roles):
            await ctx.send("What's should the role be called? This will create a new role, even if one with the same name already exists\nIf you don't want to create a new role, just type 'none'")
            response = await get_input(self, ctx)
            if response.content.lower() in ["none", "n", "no"]:
                return
            try:
                role = await guild.create_role(name=response.content)  
                roleid = role.id
            except discord.Forbidden as e:
                return await ctx.send(f"sorry that name triggered an error, please run the command again\nError: {e}")
            
            await ctx.send("and the emoji for that role?\nfor nitro users: this will only work for emojis in this server, or default emojis")
            response = await get_input(self, ctx)
            embed.add_field(name = response.content, value = role.mention, inline = False)
            try:
                await msg.add_reaction(response.content)
            except Exception as e:
                return await ctx.send(f"sorry that emoji triggered an error, please run the command again\nError: {e}")
            try:
                await msg.edit(embed = embed)
            except Exception as e:
                return await ctx.send(f"sorry there was an error editing the message, please run the command again\nError: {e}")
            
            data.append({"role_id": roleid, "emoji": response.content, "message_id": msg.id})

            with open(f"storage/reactions/roles/{ctx.channel.id}.json", "w") as f:
                json.dump(data, f)
        
        
    
    
    @commands.command(
        name="clear",
        aliases=["purge"],
        brief="Clears messages equal to the amount specified ",
    )
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=0, shut="shutupplz"):
        if amount >= 100:
            amount = 99
        if amount == 0:
            await ctx.send("please specifiy an amount")
            return
        if 0 < amount:
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

    @commands.command(name="react")
    @has_permissions(manage_messages=True)
    async def react(self, ctx, msgid = None, emoji = None):
        if msgid == None or emoji == None:
            await ctx.send("Give me a message and a reaction to react with")

        else:
            message = await ctx.fetch_message(msgid)
            await message.add_reaction(emoji)


async def open_warnings():
    with open("./storage/reports.json", encoding="utf-8") as f:
        try:
            report = json.load(f)
        except ValueError:
            report = {}
            report["users"] = []


def setup(bot):
    bot.add_cog(admin(bot))
