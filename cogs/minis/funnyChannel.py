from discord.ext import commands, tasks
import discord


class moveTaskClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.moveTask.start()

    @tasks.loop(seconds=5)
    async def moveTask(self):
        channel = self.bot.get_channel(1215738895828910080)
        await channel.edit(channel.guild.categories[0])

async def setup(bot):
    await bot.add_cog(moveTaskClass(bot))
