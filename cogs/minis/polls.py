from discord.ext import commands
import discord

letter_emote = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹"]


class polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="poll",
        brief=f'Start a poll, If no answers are provided, it will default to yes/no, Max of 20 answers\nIf answers/questions contain spaces put it in quotes\nexample: poll "Do you like bacon" yes',
    )
    @commands.guild_only()
    async def poll_command(self, ctx, question, *answers):
        """
        thanks to quantum cucumber for this code (i think it was hers at least?)
        """
        if answers == ():
            msg = await ctx.send("**📊 " + question.title() + "**")
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        elif len(answers) < 21:
            header = "**📊 " + question.title() + "**"
            inner = ""
            for i in range(len(answers)):
                inner += f"\\{letter_emote[i]} {answers[i]}\n"
            embed = discord.Embed(description=inner, colour=ctx.author.colour)
            msg = await ctx.send(header, embed=embed)
            for i in range(len(answers)):
                await msg.add_reaction(letter_emote[i])
        else:
            pass


async def setup(bot):
    await bot.add_cog(polls(bot))
