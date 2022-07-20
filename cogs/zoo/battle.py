from code import interact
from dis import dis
from email.base64mime import header_length
import discord
from discord.ui import Button, View, Select
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from io import BytesIO
import PIL

import libraries.standardLib as SL 
import libraries.animalLib as aniLib
from libraries.economyLib import *
from libraries.textBoxes import *


class zooBattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name = "battle",
        aliases = ["b"],
        brief = "fight, fight, fight",
    )
    @cooldown(2, 2, BucketType.user)
    async def battleCommand(self, ctx):
        await aniLib.open_zoo(self, ctx)
        
        #if user is None:
        user = ctx.author

        if await aniLib.check_if_zoo_not_exist(user):
            return await ctx.send("i could not find an inventory for that user, they need to create an account first")
        

        zoo = await aniLib.get_zoo_data()
        data = await aniLib.get_animal_data()
        
        team = data[str(user.id)]["team"]["members"]
        petImages = get_pets(team)
        
        teamMembers = []
        for pet in team:
            teamMembers.append(team[pet]["name"])
        
        img = PIL.Image.new('RGBA', (1440, 1100), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(img)

        text_boxes = [
            f"HP",
        ]
        
        while len(text_boxes) < len(petImages):
            text_boxes.append("")
        
        j = 0
        for i in range(250, 1070+1, 410):
            pet = PIL.Image.open(petImages[j], 'r')
            textbox = PIL.Image.new('RGBA', (pet.width*2, round(pet.height*1.5)), (255, 255, 255, 200))
            
            img.paste(pet, (i, img.height - pet.height - textbox.height - 80))
            img.paste(textbox, (i + round(pet.width / 2) - round(textbox.width / 2), img.height - textbox.height - 50))
            
            xstart:int = i + 5 + round(pet.width / 2) - round(textbox.width / 2)
            ystart:int = img.height - textbox.height - 45
            text_box(
                text_boxes[j],
                draw,
                font("storage/fonts/pixel.ttf", 24),
                (xstart, ystart, textbox.width - 10, textbox.height - 10),
                ALLIGNMENT_LEFT,
                ALLIGNMENT_TOP,
                fill=(0,0,0)
            )
            j += 1

        #background.save('temp/out.png')
        
        
        output = BytesIO()
        img.save(output, format="png")
        output.seek(0)
        
        decidedMoves = {
            "animal1": [],
            "animal2": [],
            "animal3": [],
        }
        
        async def buttonCallbackLink(interaction):
            print(teamMembers)
            print(decidedMoves)
            print(len(decidedMoves["animal1"]))
            print(len(decidedMoves["animal2"]))
            animals = ["animal1", "animal2", "animal3"]
            for animal in animals:
                if len(decidedMoves[animal]) == 0:
                    await sentMsg.reply(await SL.removeat(f"you haven't decided on a move for {teamMembers[animals.index(animal)]} yet"), delete_after=5)
                    await interaction.response.defer()
                    return
            
            await interaction.message.edit(view=view)
            await buttonCallback(interaction, teamMembers, decidedMoves) 


        async def concedeCallback(interaction):
            await ctx.send(await SL.removeat(f"{ctx.author.display_name} has decided to concede"))
            await interaction.message.edit(view=View()) # remove the inteactions on the message
            return
        async def dropDown1Link(interaction): decidedMoves["animal1"] = await dropDown(interaction, 1, teamMembers)
        async def dropDown2Link(interaction): decidedMoves["animal2"] = await dropDown(interaction, 2, teamMembers)
        async def dropDown3Link(interaction): decidedMoves["animal3"] = await dropDown(interaction, 3, teamMembers)
        
        async def getMoveInfoLink(interaction):
            id = "sting" # need do fetch this from the player data
            emoji, display_name, desc, formatting, cost, damage, healing = await getMoveInfo(id)
            for i in formatting:
                desc = desc.replace(f"({i})", str(eval(str(i))))
                
            await add_to_dropdown(1, emoji, display_name, desc, id, damage-healing, cost)
            await interaction.response.defer()
        
        confirmationButton = Button(label="Confirm Attacks", style=discord.ButtonStyle.green, emoji="⚔️")
        concedeButton = Button(label="Concede", style=discord.ButtonStyle.red, emoji="🏳️")
        test = Button(label="test", style=discord.ButtonStyle.gray, emoji="🧪")
        view = View(timeout=300,)
        view.add_item(confirmationButton)
        view.add_item(concedeButton)
        view.add_item(test)
        confirmationButton.callback = buttonCallbackLink
        concedeButton.callback = concedeCallback
        test.callback = getMoveInfoLink
        
        
        options = {
            "options1": [],
            "options2": [],
            "options3": [],
        }
            
        async def add_to_dropdown(nr, emoji, label, desc, ID, amount, cost):
            options[f"options{nr}"].append(discord.SelectOption(emoji=emoji, label=label, description=desc, value=f"{label},{ID},{amount},{cost}"))
        
        damage = 5
        cost = 3
        await add_to_dropdown(1, "⚔️", "Sting", f"charge in at the enemy, dealing {damage} damage | cost: {cost}", "attack", damage, cost)
        
        await add_to_dropdown(2, "⚔️", "Attack", "Attack", "attack", 5, 2)
        
        await add_to_dropdown(3, "⚔️", "Attack", "Attarsack", "attack", 9, 7)
        
        animal1 = Select(placeholder=f"Select a move for {teamMembers[0]}", options=options["options1"])
        animal2 = Select(placeholder=f"Select a move for {teamMembers[1]}", options=options["options2"])
        animal3 = Select(placeholder=f"Select a move for {teamMembers[2]}", options=options["options3"])
        view.add_item(animal1)
        view.add_item(animal2)
        view.add_item(animal3)
        
        animal1.callback = dropDown1Link
        animal2.callback = dropDown2Link
        animal3.callback = dropDown3Link

        sentMsg = await ctx.send(file=discord.File(output, filename="battle.png"), view=view)

        

async def getMoveInfo(id):
    with open(f"storage/battle_data/moves/{id}.json", "r") as f:
        move = json.load(f)
    

    emoji = move["emoji"]
    display_name = move["display_name"]
    desc = move["desc"]
    formatting = move["formatting"]
    cost = move["cost"]
    damage = move["damage"]
    healing = move["healing"]

    return emoji, display_name, desc, formatting, cost, damage, healing

async def buttonCallback(interaction, teamMembers, decidedMoves):
    await interaction.response.send_message(
        f"""
{teamMembers[0]} used {decidedMoves["animal1"][0]} | data: {decidedMoves["animal1"]}
{teamMembers[1]} used {decidedMoves["animal2"][0]} | data: {decidedMoves["animal2"]}
{teamMembers[2]} used {decidedMoves["animal3"][0]} | data: {decidedMoves["animal3"]}
        """)
    #await interaction.response.defer()

async def dropDown(interaction, teamNumber=0, teamMembers = []):
    #print(interaction.data)
    #print(teamNumber)
    
    values = interaction.data["values"][0].split(",")
    
    move = values[0] 
    ID = values[1]
    potency = int(values[2])
    cost = int(values[3])
    
    print(values, teamNumber)
    
    #await interaction.response.send_message(f"{teamMembers[teamNumber-1]} just used {move} for {potency} damage at the cost of {cost} mana")

    await interaction.response.defer()
    return move, ID, potency, cost

def get_pets(team):
    pets = [
        f"storage/battle_data/images/animalSprites/{team['animal1']['name'].lower()}.png",
        f"storage/battle_data/images/animalSprites/{team['animal2']['name'].lower()}.png",
        f"storage/battle_data/images/animalSprites/{team['animal3']['name'].lower()}.png",
    ]
    
    return pets
    

async def setup(bot):
    await bot.add_cog(zooBattle(bot))
