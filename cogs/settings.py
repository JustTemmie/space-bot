import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.settings import *


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        name="settings",
        aliases=["set", "config", "cfg", "setting"],
        brief="change settings for commands",
    )
    @cooldown(1, 2, BucketType.user)
    async def settingsCommand(self, ctx, category = "None", setting = "None", value = "None"):
        await store_settings(ctx.author)
        
        category = category.lower()
        setting = setting.lower()
        value = value.lower()
        

        data = await get_user_settings()
        settings = await get_all_settings()


        if category not in settings:
            embed = Embed(
                title="Categories",
                color=ctx.author.colour,
            )
            embed.set_footer(
                text=f"{ctx.prefix}{ctx.invoked_with} <Category> <Setting> <Value>\nExample: {ctx.prefix}{ctx.invoked_with} vote <Setting> <Value>"
            )
            
            for entry in settings:
                fieldDesc = ""
                for setting in settings[entry]:
                    fieldDesc += f"`{setting}`\n"
                                    
                embed.add_field(name=entry, value=fieldDesc, inline=False)
            
            await ctx.send(embed=embed)
            return


        if setting not in settings[category]:
            embed = Embed(title=f"{category} settings", color=ctx.author.color)
            embed.set_footer(text=f"{ctx.prefix}{ctx.invoked_with} <Category> <Setting> <Value>\nExample: {ctx.prefix}{ctx.invoked_with} vote reminder true")
            for child in settings[category]:
                possible_values = ""
                for value in settings[category][child]['values']:
                    possible_values += f"`{value}` "
                embed.add_field(
                    name=settings[category][child]['display_name'],
                    value=f"""
Setting: `{child}`
Value: `{str(data[str(ctx.author.id)][category][child]).lower()}`
Possible values: {possible_values}
Description: `{settings[category][child]['description']}`
                    """, inline=False)

            await ctx.send(embed=embed)
            return
        
        if value == "none":
            embed = Embed(
                title=f"`{category}` `{setting}`",
                color=ctx.author.color
            )
            embed.set_footer(
                text=f"{ctx.prefix}{ctx.invoked_with} <Category> <Setting> <Value>\nExample: {ctx.prefix}{ctx.invoked_with} {category} {setting} true"
            )
            
            embed.add_field(
                name="Current value:",
                value=f"`{str(data[str(ctx.author.id)][category][setting]).lower()}`",
                inline=False
            )
            embed.add_field(
                name="Possible values:",
                value='\n'.join(settings[category][setting]['values']),
                inline=False
            )
            embed.add_field(
                name="Description:",
                value=f"`{settings[category][setting]['description']}`",
                inline=False
            )
            await ctx.send(embed=embed)
            return


        if value not in settings[category][setting]["values"]:
            await ctx.send(f"`{value}` is not a valid value for `{category}` `{setting}`\ntry `{ctx.prefix}{ctx.invoked_with} {category} {setting}` to see all possible values")
            return

        
        if value == "true":
            value = True
        elif value == "false":
            value = False
        
        settings = await get_user_settings()
        settings[str(ctx.author.id)][category][setting] = value
        
        await ctx.send(f"`{category}` `{setting}` has been set to `{value}`")

        with open ("storage/playerinfo/settings.json", "w") as f:
            json.dump(settings, f)
        


def setup(bot):
    bot.add_cog(settings(bot))
