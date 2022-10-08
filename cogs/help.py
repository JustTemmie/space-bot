import discord
from discord.ui import Select, View
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import json

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
        embed.title = "Default Commands"
        embed.color = ctx.author.colour
        embed.description = "can't find what you're looking for? join our [support server](https://discord.gg/8MdVe6NgVy) for help"
        embed.set_footer(text = f"{ctx.prefix}help <command/category> for more info on that command or category")
        
        with open(f"storage/help_pages/Default.json", "r") as f:
            data = json.load(f)
        
        for entry in data:
            embed.add_field(name=f"{data[entry]['icon']} {data[entry]['name']}", value=data[entry]["description"], inline=False)
        
        options = [
            discord.SelectOption(
                label="Default Page",
                emoji="📚",
                description="commands that don't fit into any other catagory",
            ),
            discord.SelectOption(
                label="Economy",
                emoji="💰",
                description="info about andromeda's economy system"
            ),
        ]
        
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            options.append(
                discord.SelectOption(
                    label="Admin",
                    emoji="🛡",
                    description="administrator things"
                ),
            )
        
        set_page = Select(
            placeholder="change the current page",
            options = options   
        )

        async def set_page_func(interaction):
            if interaction.user != ctx.author:
                return

            if set_page.values[0] == "Default Page":
                page = "Default"
            elif set_page.values[0] == "Economy":
                page = "Economy"
            elif set_page.values[0] == "Admin":
                page = "Admin"
            else:
                await interaction.response.send_message("an error occured, sorry about that")
                return False

            embed.clear_fields()
            embed.title = f"{page} Commands"
            
            with open(f"storage/help_pages/{page}.json", "r") as f:
                data = json.load(f)
            
            for entry in data:
                embed.add_field(name=f"{data[entry]['icon']} {data[entry]['name']}", value=data[entry]["description"], inline=False)
            
            await msg.edit(embed=embed)
            await interaction.response.defer()
    
        set_page.callback = set_page_func
        view = View()
        view.add_item(set_page)

        msg = await ctx.send(embed=embed, view=view)
            
    
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
        
        
    @commands.command(
        name="help",
        aliases=["commands"],
        description="The help command, woah"
    )
    @cooldown(5, 35, BucketType.user)
    async def help_command(self, ctx, *, Command=None):
        if not Command:
            await self.help_no_entity(ctx)
            return

        if Command.lower() == "new commands":
            await ctx.send("category not found")
            return

        with open(f"storage/help_pages/Default.json", "r") as f:
            data = json.load(f)
        
        with open(f"storage/help_pages/Economy.json", "r") as f:
            econ_data = json.load(f)
            for i in econ_data:
                data[i] = econ_data[i]
        
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            with open(f"storage/help_pages/Admin.json", "r") as f:
                admin_data = json.load(f)
                for i in admin_data:
                    data[i] = admin_data[i]

        for nr in data:
            if data[nr]["name"].lower() == Command.lower():
                data = data[nr]
                await self.help_category(ctx, data, Command)
                return


        command = self.bot.get_command(Command)
        if command:
            await self.setup_help_pag(ctx, command)
            return

        await ctx.send("category not found")


async def setup(bot):
    await bot.add_cog(help(bot))
