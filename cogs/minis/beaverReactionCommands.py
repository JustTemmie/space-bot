from discord.ext import commands
from discord.ext.commands import cooldown, BucketType


class beavr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="beaver",
        brief="reacts with beaver to the message corresponding with the ID you send\nALTERNATIVELY the bot will react to then same message you replied to sing discord's built in feature",
    )
    @commands.guild_only()
    @cooldown(5, 10, BucketType.user)
    async def react_beaver_command(self, ctx, id=None):

        message = ctx.message
        await self.bot.http.delete_message(message.channel.id, message.id)

        if message.reference:
            id = message.reference.message_id
            message = await message.channel.fetch_message(id)
            await message.add_reaction("<a:beav:973130744190869575>")

        elif id != None:
            message = await message.channel.fetch_message(id)
            await message.add_reaction("<a:beav:973130744190869575>")

        else:
            await ctx.send(
                f"to use this command, reply to a message with {ctx.prefix}beaver",
                delete_after=7,
            )

    @commands.command(name="unbeaver", brief="beavern't")
    @cooldown(5, 10, BucketType.user)
    async def unreact_beaver_command(self, ctx, id=None):

        message = ctx.message
        await self.bot.http.delete_message(message.channel.id, message.id)

        if message.reference:
            id = message.reference.message_id
            message = await message.channel.fetch_message(id)
            await message.remove_reaction("<a:beav:973130744190869575>", self.bot.user)

        elif id != None:
            message = await message.channel.fetch_message(id)
            await message.remove_reaction("<a:beav:973130744190869575>", self.bot.user)

        else:
            await ctx.send(
                f"to use this command, reply to a message with {ctx.prefix}beaver",
                delete_after=7,
            )


async def setup(bot):
    await bot.add_cog(beavr(bot))
