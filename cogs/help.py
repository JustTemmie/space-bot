from sre_parse import CATEGORIES
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.buttons import Paginator

import json
import os


# WARNING this code is bad lmao
# it's old and i updated it later on, a lot of this is unused :p

class Page(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


class help(commands.Cog, name="Help command"):
    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 7

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}\n{command.description}"
        return signature

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue

                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue

        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def setup_help_pag(self, ctx, entity=None, title=None):
        entity = entity or self.bot
        title = title or self.bot.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values())) if hasattr(entity, "all_commands") else []
            )
            filtered_commands.insert(0, entity)

        else:
            filtered_commands = await self.return_filtered_commands(entity, ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i : i + self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                desc = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd, ctx)
                subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

                commands_entry += (
                    f"{ctx.prefix} **__{cmd.name}__**\n{signature}\n```\n{desc}\n"
                    if isinstance(entity, commands.Command)
                    else f"{ctx.prefix} **__{cmd.name}__**\n{desc}\n {subcommand}\n"
                )
            pages.append(commands_entry)
        
        await Page(title=title, suffix="can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help", colour=ctx.author.colour, entries=pages, length=1).start(ctx)


    async def help_no_entity(self, ctx):
        embed = discord.Embed()
        embed.title = "Commands"
        embed.color = ctx.author.colour
        embed.description = "Can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        embed.set_footer(text = f"{ctx.prefix}help <command/category> for more info on that command or category")
        
        with open(f"storage/help_pages/everyone.json", "r") as f:
            data = json.load(f)
        
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            with open(f"storage/help_pages/admin.json", "r") as f:
                admin_data = json.load(f)
            
            for i in admin_data:
                data[i] = admin_data[i]

        for entry in data:
            embed.add_field(name=f"{data[entry]['icon']} {data[entry]['name']}", value=data[entry]["description"], inline=False)


        await ctx.send(embed=embed)
            
    
    async def help_category(self, ctx, data, entity):
        embed = discord.Embed()
        embed.title = f"{data['icon']} {data['name']}"
        embed.description = "Can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        
        commands = data["description"]
        commands = commands.split(" ")

        
        cmds = self.bot.commands
        cmdnames = []
        for cmd in cmds:
            cmdnames.append(cmd.name.lower())
        for entry in commands:
            #print(entry)
            #if entry in cmdnames:
                #print("a")
                for cmd in cmds:
                    if cmd.name.lower() == entry[1:-1].lower():
                        desc = cmd.brief# + "\n" + cmd.description
                        
                        
                        embed.add_field(name=entry, value=desc, inline=False)
    
        await ctx.send(embed=embed)
        
        
    @commands.command(name="help", aliases=["commands"], description="The help command, woah")
    @cooldown(5, 35, BucketType.user)
    async def help_command(self, ctx, *, entity=None):
        if not entity:
            await self.help_no_entity(ctx)
            return


        with open(f"storage/help_pages/everyone.json", "r") as f:
            data = json.load(f)
        
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            with open(f"storage/help_pages/admin.json", "r") as f:
                admin_data = json.load(f)
                for i in admin_data:
                    data[i] = admin_data[i]

        for nr in data:
            if data[nr]["name"].lower() == entity.lower():
                data = data[nr]
                await self.help_category(ctx, data, entity)
                return


        command = self.bot.get_command(entity)
        if command:
            await self.setup_help_pag(ctx, command, command.name)
            return

        await ctx.send("cog not found")


def setup(bot):
    bot.add_cog(help(bot))
