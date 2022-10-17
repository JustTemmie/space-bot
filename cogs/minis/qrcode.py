import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import libraries.standardLib as SL

import qrcode
import cv2


class qrcodegenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="qr",
        brief="Give it a string and it'll return you a qr code]\nIt can also decode a qr code and return it as a message",
    )
    @cooldown(1, 3, BucketType.user)
    async def qrcode(self, ctx, *, input=None):
        if ctx.message.attachments != []:
            image = ctx.message.attachments[0]

            if image.size > 1048576:
                await ctx.send("Sorry, that image is too big")
                return

            await image.save(f"temp/qrinput{ctx.author.id}.png")

            filename = f"temp/qrinput{ctx.author.id}.png"
            # read the QRCODE image
            image = cv2.imread(filename)
            # initialize the cv2 QRCode detector
            detector = cv2.QRCodeDetector()
            # detect and decode
            data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

            if vertices_array is not None:
                await ctx.reply(await SL.removeat(data))
            else:
                await ctx.reply("sorry, no QR code found")

            return

        if input == None:
            await ctx.send(
                "Please give me a string to generate a qr code for\nOr attach a qr code in your message and i'll decode it for you"
            )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(str(input))
        try:
            qr.make(fit=True)
        except Exception as e:
            return await ctx.send(f"Error: {e}\nThe string is likely too long, sorry about that")

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        img.save("temp/qrcode.png")
        await ctx.send(file=discord.File("temp/qrcode.png"))


async def setup(bot):
    await bot.add_cog(qrcodegenerator(bot))
