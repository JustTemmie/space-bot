from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from typing import Optional
from datetime import datetime


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="userinfo",
        aliases=["memberinfo", "who", "ui", "mi"],
        brief="Tells you a bunch of info about a specified user",
    )
    @cooldown(3, 10, BucketType.guild)
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(
            title="User info",
            colour=target.colour,
            timestamp=datetime.utcnow(),
        )

        fields = [
            ("ID", target.id, True),
            ("Name", str(target), True),
            ("Bot?", target.bot, True),
            ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Boosting", bool(target.premium_since), True),
            ("Status", str(target.status).title(), True),
            (
                "Activity",
                f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ' '}",
                True,
            ),
            ("Top role", target.top_role.mention, True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

            embed.set_thumbnail(url=target.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        name="serverinfo",
        aliases=["guildinfo", "si", "gi"],
        brief="Tells you a bunch of random info about the server",
    )
    @commands.guild_only()
    async def server_info(self, ctx):
        embed = Embed(
            title="Server info",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )

        statuses = [
            len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        ]

        fields = [
            ("ID", ctx.guild.id, True),
            ("Owner", ctx.guild.owner, True),
            ("Region", ctx.guild.region, True),
            ("Members", len(ctx.guild.members), True),
            ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
            ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
            ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            # ("Banned members", len(await ctx.guild.bans()), True),
            ("Roles", len(ctx.guild.roles), True),
            (
                "Statuses",
                f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}",
                True,
            ),
            ("Text channels", len(ctx.guild.text_channels), True),
            ("Voice channels", len(ctx.guild.voice_channels), True),
            ("Categories", len(ctx.guild.categories), True),
            # ("Invites", len(await ctx.guild.invites()), True),
            # ("Admins", ("<@368423564229083137>, <@645969806104723456>, and <@689565874612469784>")),
            # ("\u200b", "\u200b", True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
