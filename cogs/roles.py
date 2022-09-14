import discord
from discord.ext import commands

import json


class role_menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        
        with open("storage/reactions/channels.json", "r") as f:
            channels = json.load(f)
            if payload.channel_id not in channels["channels"]:
                return
        
        channel = payload.channel_id

        
        with open(f"./storage/reactions/roles/{channel}.json") as react_file:
            data = json.load(react_file)

        try:
            for x in data:
                #print(x["emoji"], payload.emoji.name)
                if x["emoji"] == payload.emoji.name:
                    role = payload.member.guild.get_role(x["role_id"])
                    await payload.member.add_roles(role)
        
        except Exception as e:
            print(f"no role found, line 40ish roles.py {e}")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, payload):
        
        with open("storage/reactions/channels.json", "r") as f:
            channels = json.load(f)
            if payload.channel_id not in channels["channels"]:
                return

        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        with open(f"./storage/reactions/roles/{payload.channel_id}.json") as react_file:
            data = json.load(react_file)
            
        for x in data:
            if x["emoji"] == payload.emoji.name:
                role = discord.utils.get(
                    self.bot.get_guild(payload.guild_id).roles, id=x["role_id"]
                )
                await member.remove_roles(role)


async def setup(bot):
    await bot.add_cog(role_menu(bot))
