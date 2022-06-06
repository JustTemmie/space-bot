from discord.ext import commands
import discord

letter_emote = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹"]


class polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="poll",
        brief=f'Start a poll, If no answers are provided, it will default to yes/no, Max of 10 answers\nIf answers/questions contain spaces put it in quotes\nexample: poll "Do you like bacon" yes',
    )
    async def poll_command(self, ctx, question, *answers):
        """
        Start a poll.

        If no answers are provided, it will default to yes/no
        Max of 10 answers
        If answers/questions contain spaces put it in quotes
        e.g. >poll "Do you like bacon" yes
        """
        if answers == ():
            msg = await ctx.send("**📊 " + question.title() + "**")
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        elif len(answers) < 21:
            header = "**📊 " + question.title() + "**"
            inner = ""
            for i in range(len(answers)):
                inner += f"\\{letter_emote[i]} {answers[i].title()}\n"
            embed = discord.Embed(description=inner, colour=0x02389E)
            msg = await ctx.send(header, embed=embed)
            for i in range(len(answers)):
                await msg.add_reaction(letter_emote[i])
        else:
            pass


def setup(bot):
    bot.add_cog(polls(bot))
