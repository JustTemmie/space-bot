import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from io import BytesIO
import PIL

import libraries.standardLib as SL 
import libraries.animalLib as aniLib
from libraries.economyLib import *
from libraries.textBoxes import *


# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


# Define a simple View that gives us a counter button
class Counter(discord.ui.View):

    # Define the actual button
    # When pressed, this increments the number displayed until it hits 5.
    # When it hits 5, the counter button is disabled and it turns green.
    # note: The name of the function does not matter to the library
    @discord.ui.button(label='0', style=discord.ButtonStyle.red)
    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
        number = int(button.label) if button.label else 0
        if number + 1 >= 5:
            button.style = discord.ButtonStyle.green
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)



class Dropdown(discord.ui.Select):
    def __init__(self, DropDown1 = "red", DropDown2 = "green", DropDown3 = "blue", memberID = ""):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label=DropDown1, description='Your favourite colour is red', emoji='🟥'),
            discord.SelectOption(label=DropDown2, description='Your favourite colour is green', emoji='🟩'),
            discord.SelectOption(label=DropDown3, description='Your favourite colour is blue', emoji='🟦'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder=f'Action for friend nr {memberID}', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')

class selfMade(discord.ui.View):
    def __init__(self):
        super().__init__()
        
        self.add_item(Dropdown("i", "like", "trains", 1))
        self.add_item(Dropdown("this", "is a", "test", 2))
        self.add_item(Dropdown("this", "is a", "test", 3))
        
    @discord.ui.button(label='Confirm Actions', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.stop()


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
        
        img = PIL.Image.new('RGBA', (1440, 1100), (0, 0, 0, 0))
        
        #font = PIL.ImageFont.truetype("storage/fonts/pixel.ttf", 24)
        draw = PIL.ImageDraw.Draw(img)
        
        
        team = data[str(user.id)]["team"]["members"]

        pets = [
            f"storage/battle_data/images/{team['animal1']['name'].lower()}.png",
            f"storage/battle_data/images/{team['animal2']['name'].lower()}.png",
            f"storage/battle_data/images/{team['animal3']['name'].lower()}.png",
        ]
        
        text_boxes = [
            f"HP",
        ]
        
        while len(text_boxes) < len(pets):
            text_boxes.append("")
        
        j = 0
        for i in range(250, 1070+1, 410):
            pet = PIL.Image.open(pets[j], 'r')
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
        
        buttons = selfMade()
        await ctx.send(file=discord.File(output, filename="battle.png"), view=buttons)
        
        # await buttons.wait()
        # if buttons.value is None:
        #     await ctx.send('Timed out...')
        # elif buttons.value:
        #     await ctx.send('Confirmed...')
        # else:
        #     await ctx.send('Cancelled...')
        
        
        
        #img.show()     
        

async def setup(bot):
    await bot.add_cog(zooBattle(bot))
