import discord
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import (
    Cog,
    Greedy,
    cooldown,
    BucketType,
    CheckFailure,
    command,
    has_permissions,
    bot_has_permissions,
)
import json
import time

from libraries.miscLib import get_input


class admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="prefix",
        aliases=["prefixes", "setprefix", "andro_prefix"],
        brief="Sets the prefix for the bot in this server",
    )
    @cooldown(1, 1.5, BucketType.user)
    @has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix: str = None):
        with open("storage/guild_data/prefixes.json", "r") as f:
            prefixes = json.load(f)

        try:
            prefixes[str(ctx.guild.id)]
        except:
            prefixes[str(ctx.guild.id)] = {}
            prefixes[str(ctx.guild.id)]["prefix1"] = "a!"
            prefixes[str(ctx.guild.id)]["prefix2"] = "none"
            prefixes[str(ctx.guild.id)]["prefix3"] = "none"
            prefixes[str(ctx.guild.id)]["prefix4"] = "none"
            prefixes[str(ctx.guild.id)]["prefix5"] = "none"

            with open("storage/guild_data/prefixes.json", "w") as f:
                json.dump(prefixes, f)

        if prefix is not None:
            try:
                index = int(prefix[0])
                if prefix[1] == " ":
                    prefix = prefix[2:]
                else:
                    prefix = prefix[1:]
            except:
                index = 0
                for prx in prefixes[str(ctx.guild.id)]:
                    index += 1
                    if prefixes[str(ctx.guild.id)][prx] == "none":
                        break

            if index > 5:
                await ctx.send(
                    f"There are only 5 prefixes available\nPlease use a prefix that is not already in use, or overwrite an existing one {ctx.prefix}{ctx.invoked_with} 2 {prefix}"
                )

            elif prefix == "clear":
                prefixes[str(ctx.guild.id)]["prefix1"] = "a!"
                prefixes[str(ctx.guild.id)]["prefix2"] = "none"
                prefixes[str(ctx.guild.id)]["prefix3"] = "none"
                prefixes[str(ctx.guild.id)]["prefix4"] = "none"
                prefixes[str(ctx.guild.id)]["prefix5"] = "none"

            else:
                prefixes[str(ctx.guild.id)][f"prefix{index}"] = prefix

        embed = Embed(
            title="Prefixes",
            # description=f"Prefixes for this server: ",
            color=ctx.author.color,
        )
        embed.description = f'To clear the prefixes, use {ctx.prefix}{ctx.invoked_with} clear, this will still leave "a!" as the a prefix\nTo overwrite a prefix, use {ctx.prefix}{ctx.invoked_with} index <prefix>, this can also be set to "none" in order to clear it\nExample {ctx.prefix}{ctx.invoked_with} 2 none\n\nIf you clear all prefixes pinging the bot will still be a valid prefix\nExample @andromeda prefix'

        for i, prefix in enumerate(prefixes[str(ctx.guild.id)]):
            if prefix.lower() == "none":
                prefix = prefix.lower()
            embed.add_field(name=f"prefix {i+1}", value=f"`{prefixes[str(ctx.guild.id)][prefix]}`", inline=False)

        await ctx.send(embed=embed)

        with open("storage/guild_data/prefixes.json", "w") as f:
            json.dump(prefixes, f)

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

                embed.set_thumbnail(url=target.display_avatar.url)
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

            embed.set_thumbnail(url=target.display_avatar.url)
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

        max_roles = 20
        funnystr = ""

        deled = await ctx.send("What should the name of the role menu/embed be?", delete_after=45)
        response = await get_input(self, ctx, 45)
        embed = discord.Embed(title=response.content, color=0x00FF00)
        msg = await ctx.send(embed=embed)
        await deled.delete()
        await response.delete()

        deled = await ctx.send(
            "What should the description of the role menu/embed be? if you don't want one, just type 'none'",
            delete_after=45,
        )
        response = await get_input(self, ctx, 45)
        await deled.delete()
        if not response.content.lower() in ["none", "n", "no"]:
            embed.description = response.content
        await msg.edit(embed=embed)
        await response.delete()

        try:
            with open(f"storage/reactions/roles/{ctx.channel.id}.json", "r") as f:
                data = json.load(f)
        except:
            with open(f"storage/reactions/roles/{ctx.channel.id}.json", "w") as f:
                data = []

        with open(f"storage/reactions/channels.json", "r") as f:
            channels = json.load(f)

        if not ctx.channel.id in data:
            channels["channels"].append(ctx.channel.id)
            with open(f"storage/reactions/channels.json", "w") as f:
                json.dump(channels, f)

        for i in range(max_roles):
            deled = await ctx.send(
                "What's should the role be called? This will create a new role, even if one with the same name already exists\nIf you don't want to create a new role, just type 'none'",
                delete_after=150,
            )
            response = await get_input(self, ctx, 150)
            await deled.delete()
            await response.delete()
            if response.content.lower() in ["none", "n", "no"]:
                return await ctx.send("Role menu creation completed, users can now react to the message to get roles", delete_after=20)
            try:
                role = await ctx.guild.create_role(name=response.content)
                roleid = role.id
            except discord.Forbidden as e:
                return await ctx.send(f"sorry that name triggered an error, please run the command again\nError: {e}")

            deled = await ctx.send(
                "and the emoji for that role?\nfor nitro users: this will only work for emojis in this server, or default emojis",
                delete_after=150,
            )
            response = await get_input(self, ctx, 150)
            await deled.delete()
            await response.delete()

            funnystr += f"{response.content} {role.mention}\n"
            embed.clear_fields()
            embed.add_field(name="||\n||", value=funnystr, inline=False)
            try:
                await msg.add_reaction(response.content)
            except Exception as e:
                return await ctx.send(f"sorry that emoji triggered an error, please run the command again\nError: {e}")
            try:
                await msg.edit(embed=embed)
            except Exception as e:
                return await ctx.send(f"sorry there was an error editing the message, please run the command again\nError: {e}")

            data.append({"role_id": roleid, "emoji": response.content, "message_id": msg.id})

            with open(f"storage/reactions/roles/{ctx.channel.id}.json", "w") as f:
                json.dump(data, f)

    @commands.command(name="nonimagepurge", aliases=["ipurge"], brief="clears all X last messages that don't have an image attatched")
    @bot_has_permissions(manage_messages=True)
    # @has_permissions(manage_messages=True)
    async def nonimagepurge(self, ctx, amount=0):
        if amount >= 100:
            amount = 99

        if amount <= 0:
            await ctx.send("please specifiy an amount")
            return

        if 0 < amount:
            channel = ctx.message.channel
            messages = []
            async for message in channel.history():
                if len(message.attachments) == 0 and len(message.embeds) == 0:
                    # if the message is over 14 days old, don't
                    if time.mktime(message.created_at.timetuple()) + 1209500 < int(time.time()):
                        break
                    messages.append(message)
                    if len(messages) >= amount + 1:
                        break

            purged = len(messages)

            await channel.delete_messages(messages)
            await ctx.send(
                f"{purged} messages have been purged by {ctx.message.author.mention}",
                delete_after=10,
            )
            if purged != amount + 1:
                await ctx.send("cannot delete messages that are more than 14 days old, sorry", delete_after=10)

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")

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
    async def react(self, ctx, msgid=None, emoji=None):
        if msgid == None or emoji == None:
            await ctx.send("Give me a message and a reaction to react with")
            return

        try:
            message = await ctx.fetch_message(msgid)
            await message.add_reaction(emoji)
        except Exception as e:
            await ctx.send(f"Error: {e}", delete_after=20)


async def open_warnings():
    with open("./storage/reports.json", encoding="utf-8") as f:
        try:
            report = json.load(f)
        except ValueError:
            report = {}
            report["users"] = []


async def setup(bot):
    await bot.add_cog(admin(bot))
