from curses.ascii import EM
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import psutil
import platform
from datetime import datetime


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


class hw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # https://www.thepythoncode.com/article/get-hardware-system-information-python
    @commands.command(
        name="info",
        aliases=["information", "status"],
        brief="Get info about the bot",
    )
    @cooldown(8, 120, BucketType.user)
    async def info_command(self, ctx, page=1):
        pages = 4

        Embed = discord.Embed(title="Info", color=0x00FF00)
        Embed.set_footer(text=f"page {page} of {pages}")

        if page == 1:
            page_info = "**General info**"
            uname = platform.uname()
            cpufreq = psutil.cpu_freq()
            svmem = psutil.virtual_memory()
            Embed.add_field(
                name="System",
                value=f"{uname.node} {uname.system} {uname.release}",
                inline=False,
            )
            Embed.add_field(
                name="Processor",
                value=f"{uname.processor} at {int(cpufreq.max)}MHz",
                inline=False,
            )
            Embed.add_field(name="Memory", value=f"{get_size(svmem.total)}", inline=False)
            Embed.add_field(
                name="Disk",
                value=f"{get_size(psutil.disk_usage('/').total)}",
                inline=False,
            )
            Embed.add_field(
                name="Uptime",
                value=f"{datetime.now() - datetime.fromtimestamp(psutil.boot_time())}",
                inline=False,
            )

        elif page == 2:
            page_info = "**CPU info**"
            Embed.add_field(
                name="Physical cores",
                value=psutil.cpu_count(logical=False),
                inline=False,
            )
            Embed.add_field(name="Total cores:", value=psutil.cpu_count(logical=True), inline=False)

            cpufreq = psutil.cpu_freq()
            Embed.add_field(name="Max Frequency", value=f"{cpufreq.max:.2f}Mhz", inline=False)
            Embed.add_field(name="Min Frequency", value=f"{cpufreq.min:.2f}Mhz", inline=False)
            Embed.add_field(
                name="Current Frequency",
                value=f"{(cpufreq.current)*1000:.2f}Mhz",
                inline=False,
            )

            Embed.add_field(name="Total CPU Usage", value=f"{psutil.cpu_percent()}%", inline=False)
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                Embed.add_field(name=f"Core {i}", value=f"{percentage}%")

        elif page == 3:
            page_info = "**Memory info**"
            svmem = psutil.virtual_memory()
            Embed.add_field(name="Total", value=f"{get_size(svmem.total)}", inline=False)
            Embed.add_field(name="Available", value=f"{get_size(svmem.available)}", inline=False)
            Embed.add_field(name="Used", value=f"{get_size(svmem.used)}", inline=False)
            Embed.add_field(name="Percentage", value=f"{svmem.percent}%", inline=False)
            # get the swap memory details (if exists)
            swap = psutil.swap_memory()
            Embed.add_field(name="Total Swap", value=f"{get_size(swap.total)}", inline=False)
            Embed.add_field(name="Free Swap", value=f"{get_size(swap.free)}", inline=False)
            Embed.add_field(name="Used Swap", value=f"{get_size(swap.used)}", inline=False)
            Embed.add_field(name="Used Swap Percentage", value=f"{swap.percent}%", inline=False)

        elif page == 4:
            page_info = "**Misc info**"
            Embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
            Embed.add_field(name="Python", value=f"{platform.python_version()}", inline=False)
            Embed.add_field(name="Shards", value=f"{self.bot.shard_count}", inline=False)
            Embed.add_field(name="Current Shard", value=f"{ctx.guild.shard_id+1}", inline=False)
            Embed.add_field(name="Discord.py", value=f"{discord.__version__}", inline=False)
            Embed.add_field(name="Cogs", value=f"{len(self.bot.cogs)}", inline=False)
            Embed.add_field(name="Commands", value=f"{len(self.bot.commands)}", inline=False)
            Embed.add_field(name="Guilds", value=f"{len(self.bot.guilds)}", inline=False)
            Embed.add_field(name="Users", value=f"{len(self.bot.users)}", inline=False)
            Embed.add_field(name="Owner", value=f"Temmie#0001", inline=False)
            Embed.add_field(
                name="Github",
                value=f"https://github.com/JustTemmie/space-bot",
                inline=False,
            )

        else:
            await ctx.send("Invalid page")
            return

        Embed.description = (
            f"information about the server {self.bot.user.name} is running on\n\n{page_info}"
        )
        await ctx.send(embed=Embed)


def setup(bot):
    bot.add_cog(hw(bot))
