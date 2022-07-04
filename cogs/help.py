import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import json


# WARNING this code is bad lmao
# it's old and i updated it later on, a lot of this is unused :p


class help(commands.Cog, name="Help command"):
    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 7
    

    async def setup_help_pag(self, ctx, entity=None):        
        embed = discord.Embed()
        embed.title = f"{entity.name}"
        embed.description = "can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        
        embed.add_field(
            name = "usage:",
            value = f"{ctx.prefix}{entity.name} {entity.signature}",
            inline = False
        )
        
        if entity.aliases:
            embed.add_field(
                name = "aliases:",
                value = f"{', '.join(entity.aliases)}",
                inline = False
            )

        if entity.brief:
            embed.add_field(
                name = "description:",
                value = f"{entity.brief}",
                inline = False
            )

        if entity.usage:
            embed.add_field(
                name = "usage:",
                value = f"{entity.usage}",
                inline = False
            )
        
        if entity.cooldown:
            value = f"{entity.cooldown.rate} times per {entity.cooldown.per} seconds"
            embed.add_field(
                name = "cooldown:",
                value = f"{value}",
                inline = False
            )
        
        await ctx.send(embed=embed)
        
        return

    async def help_no_entity(self, ctx):
        embed = discord.Embed()
        embed.title = "Commands"
        embed.color = ctx.author.colour
        embed.description = "can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        embed.set_footer(text = f"{ctx.prefix}help <command/category> for more info on that command or category")
        
        with open(f"storage/help_pages/everyone.json", "r") as f:
            data = json.load(f)
        
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            with open(f"storage/help_pages/admin.json", "r") as f:
                admin_data = json.load(f)
            
            for i in admin_data:
                data[i] = admin_data[i]

        for entry in data:
            embed.add_field(name=f"{data[entry]['icon']} {data[entry]['name']}", value=data[entry]["description"], inline=False)


        await ctx.send(embed=embed)
            
    
    async def help_category(self, ctx, data, entity):
        embed = discord.Embed()
        embed.title = f"{data['icon']} {data['name']}"
        embed.description = "can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        
        commands = data["description"]
        commands = commands.split(" ")

        
        cmds = self.bot.commands
        cmdnames = []
        for cmd in cmds:
            cmdnames.append(cmd.name.lower())
        for entry in commands:
            #print(entry)
            #if entry in cmdnames:
                #print("a")
                for cmd in cmds:
                    if cmd.name.lower() == entry[1:-1].lower():
                        desc = cmd.brief# + "\n" + cmd.description
                        
                        
                        embed.add_field(name=entry, value=desc, inline=False)
    
        await ctx.send(embed=embed)
        
        
    @commands.command(name="help", aliases=["commands"], description="The help command, woah")
    @cooldown(5, 35, BucketType.user)
    async def help_command(self, ctx, *, entity=None):
        if not entity:
            await self.help_no_entity(ctx)
            return


        with open(f"storage/help_pages/everyone.json", "r") as f:
            data = json.load(f)
        
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            with open(f"storage/help_pages/admin.json", "r") as f:
                admin_data = json.load(f)
                for i in admin_data:
                    data[i] = admin_data[i]

        for nr in data:
            if data[nr]["name"].lower() == entity.lower():
                data = data[nr]
                await self.help_category(ctx, data, entity)
                return


        command = self.bot.get_command(entity)
        if command:
            await self.setup_help_pag(ctx, command)
            return

        await ctx.send("cog not found")


async def setup(bot):
    await bot.add_cog(help(bot))
