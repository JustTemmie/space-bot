import discord
from discord.ext import commands
from discord.utils import get

import json


class role_menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        
        channel_IDS = [
            919714824915648562,
            849692162907176990,
            956467944991358997
        ]
        
        role_directories = [
            "frog_reactions",
            "space_reactions",
            "castle_reactions"
        ]
        
        if payload.channel_id not in channel_IDS:
            return
        
        for channel_ID, dir in zip(channel_IDS, role_directories):
            if payload.channel_id == (channel_ID):  # frog
                with open(f"./storage/reactions/{dir}.json") as react_file:
                    data = json.load(react_file)

        try:
            for x in data:
                if x["emoji"] == payload.emoji.name:
                    role = get(payload.member.guild.roles, id=x["role_id"])
                    await payload.member.add_roles(role)
                    print(f"added {role}")
        
        except:
            print("no role found, line 40ish roles.py")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id == (919714824915648562):  # frog
            with open("./storage/reactions/frog_reactions.json") as react_file:
                data = json.load(react_file)

        elif payload.channel_id == (849692162907176990):  # space
            with open("./storage/reactions/space_reactions.json") as react_file:
                data = json.load(react_file)

        elif payload.channel_id == (956467944991358997):  # crawford castle
            with open("./storage/reactions/castle_reactions.json") as react_file:
                data = json.load(react_file)

        else:
            return

        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        for x in data:
            if x["emoji"] == payload.emoji.name:
                role = discord.utils.get(
                    self.bot.get_guild(payload.guild_id).roles, id=x["role_id"]
                )
                await member.remove_roles(role)
                print(f"removed {role}")


def setup(bot):
    bot.add_cog(role_menu(bot))
