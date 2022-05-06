import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.buttons import Paginator

# from utilities import Page

# i honestly have no idea how this code works, if you have problems with it, i can't help you


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

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"
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

        await Page(title=title, colour=ctx.author.colour, entries=pages, length=1).start(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        print("cogs online")

    @commands.command(name="help", aliases=["commands"], description="The help command, woah")
    @cooldown(5, 35, BucketType.user)
    async def help_command(self, ctx, *, entity=None):
        if not entity:
            cog_embed = Embed(
                title="Cogs to call upon",
                description='these are the categories you can use with the help command, for example "!help economy" would bring back all commands related to money',
                colour=0xAF62EB,
            )

            fields = [  # ("Name", "Value", True),
                ("admin", "commands for admins", True),
                ("economy", "all commands related to money", False),
                (
                    "fun",
                    "just random commands i've added, like wikipedia and fact",
                    True,
                ),
                ("images", "lets you do stuff with images", False),
                (
                    "info",
                    "commands that give you information about something - currently broken",
                    True,
                ),
                ("utility", "utility commands like setting a reminder", False),
                ("misc", "mostly empty, for now", False),
                (
                    "search",
                    "commands that let you search stuff like youtube or wikipedia",
                    False,
                ),
                ("other cogs", "polls, prefix, reactions, events, and help", False),
            ]

            for name, value, inline in fields:
                cog_embed.add_field(name=name, value=value, inline=inline),
                cog_embed.set_author(name=(ctx.author)),
                cog_embed.set_footer(text="Sent from my iPhone"),
                cog_embed.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/765222621779853312/07d33473a5a8b5fa6adf600967f7692e.png?size=2048"
                )

            await ctx.send(embed=cog_embed)
            await self.setup_help_pag(ctx)

        else:
            cog = self.bot.get_cog(entity)
            if cog:
                await self.setup_help_pag(ctx, cog, f"{cog.qualified_name}'s commands")

            else:
                command = self.bot.get_command(entity)
                if command:
                    await self.setup_help_pag(ctx, command, command.name)

                else:
                    await ctx.send("entity not found")


def setup(bot):
    bot.add_cog(help(bot))
