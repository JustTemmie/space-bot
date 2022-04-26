import discord
from discord.ext import commands, tasks
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, cooldown, BucketType
import random
from datetime import datetime

IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

import requests
import json
import os
from dotenv import load_dotenv
load_dotenv("TENOR_API_KEY.env")
tenor_api_key = os.getenv("KEY")


henwees = [
    "henwee :)",
    "henw",
    "green h man my beloved <3",
    "him",
    "what if shenwee tho??",
    "😳",
    "henwee is cool and all, but fuck C",
    "hewwow :)",
    "himwee",
    "smilewee",
    ":)wee",
    "the him",
    "little baby man",
    "little bitch",
    "joker lover 182",
    "he can draw bird :)",
    "wee wee",
    "oui oui",
    "theynwee",
    "\"the xwees\"",
    "fuckin unity loser lmao imagine using a program with a scuffed cube as an icon smh my head",
    "brib",
    "uwu",
    "ÆwÆ",
    "\"Being harassed is dumb people shiz\" ",
    "look at him roll :)",
    "breast cheese 😋",
    "the man who never eats a måltid",
    "\"cheese is just cow-breast-cheese\"",
    "\"man is the best gender\"",
    "bitchass gorou simp",
    "\"feeler shit, man\"",
    "\"duuuu, thinkeeeeer\"",
    "this isn't henwee related i just wanted to say hi geek :)",
    "owo",
    "anywho, beaver clicker",
    "m a n",
    "man",
    "fis :)",
    "\"https://store.steampowered.com/app/1718240/Beaver_Clicker/\" - Henwee 2022",
    "\"flushed best emoji confirmed\"",
    "henwy is just some youtuber",
    "<a:henwee_fall:955830194902544415>",
    "henwee spin",
    "please i'm running out of things to put here fajsfdkans nnuwiuab lvbseru sroveronaewruocnweou fuipasn coewivop8aew oaer nuoaern voaernv oer noåerunc voewurnv"
    "holy fuck please stop with the genshin mr hen hen",
    "weehen",
    "beawee:)",
    "gorou 2",
    "gay lil bebi fis",
    "funny fis fredaaag",
    "🏾",
    "🦫",
    "<:wishlistbeaverclickeronsteam:943915845023846401>",
    "the crippledest man in the west",
    "Playing Genshin Impact",
    "\"a\" -hen 2022",
    "\"psfttthhh i dunnu\" -hen 2022",
    "\"\⬛\" -hen 2022",
    "\"who tf put the physical theorapist 5 stories up?\" -hen 2022",
    "\"ok fair\" -hen 2022",
    "\"yes these kids suck lmao\" -hen 2022",
    "\"tell me how thaumaturgy and prestidigitation is \"utility\", but druidcraft is \"control\"\" -hen 2022",
    "\"mean ):\" -hen 2022",
    "\"i feel like i should mention, lillevi and korede isn't here (😠)\" -hen 2022",
    "\"most things, except liquorice\" -hen 2022",
    "\"Gonna go touch it\" -hen 2022",
    "\"well i'm touchable, but I won't be hurt\" -hen 2022",
    "\"BTW I'm not coming to school tomorrow with a lesbian haircut\" -hen 2022",
    "\"remember, everyone who doesn't say anything agrees, just ask Elly\" -hen 2022",
    "\"js is a shithole hellscape\n(which is nothing like c# i promise)\" -hen 2022",
    "\"uglies shit i've seen\" -hen 2022",
    "\"USA er under india\" -hen 2022",
    "\"not noticed that, so I guess it's less noticable\" - hen 2022",
    "\"i dag seiner tidlig\" - not hen 2022",
    "\“blaze can go ******* ***** ***** ********************\” - hen 2022",
    "\“I mean walking is nice\nMiss being able to\”\n- henw2022",
    "\"I'd fuck joker from persona 5\"\n\"I'd be fucked by joker from persona 5\"\n- hen 2022",
    "\"You're like one foot in the grave, the other in the closet\" - related to hen 2022 ",
    "\"æ har ingen oppion om uteliggere\" - hen 2022",
    "\"no\" - hen 2022",
    "\"what\" - hen 2022",
    "\"æ skippe alltid denne delen av biler 1\" - hen 2022",
    "\"du kan ikke bare si [...]\" - hen 2022",
    "\"genshin impact e trash\" - hen 2022",
    "\"cumfused\" - hen 2022",
    "\"hvor mye packer lightning mcqueen?\" - hen 2022",
    "\"revert revert actually fixed collison\" - hen 2022",
    "\"æ hate barn, æ hate barn\" - hen 2022",
    "\"🦫\" - not hen 2022",
    "\"henwee quote\" - hen 2022",
    "\"æ like fugla deez nuts\" - hen 2022",
    "\"time to commit mass suicide\" - hen 2022",
    "\"put de som en quote\" - hen 2022",
    "\"https://cdn.discordapp.com/attachments/847231965764780063/966342099043753984/unknown.png\" - hen 2022",
    "\"you're a fucking idiot\" - hen 2022",
    

    #copilot lmao
    "\"i'm not a fan of the word \"fucking\"\" -hen 2022 - github copilot",
    "\“I'm not a fan of the word \"utility\"\” - hen 2022 - github copilot",
    "\“I'm not a fan of the word \"control\"\” - hen 2022 - github copilot",
    "\"my body is a trashcan\" - hen 2022 - github copilot",
    "\"joker is a trash\" - hen 2022 - github copilot",
    "\"henwee is a trash\" - hen 2022 - github copilot",


    
]




class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.henwee.start()
        self.random_beaver.start()



    @commands.Cog.listener()
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Sorry, something unexpected went wrong.")
            #raise

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            #await ctx.send("Sorry, I couldn't find that command")
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(
                f"One or more of the required arguments are missing, perhaps the help command could help you out? {ctx.prefix}help (command)"
            )

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Please try again in {exc.retry_after:,.2f} seconds.",
                delete_after=(exc.retry_after + 0.7))

    #      elif isinstance(exc.original, HTTPException):
    #          await ctx.send("Unable to send message.")

        elif hasattr(exc, "original"):
            #raise exc  # .original

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have the permission to do that.")

            else:
                raise exc.original

        else:
            raise exc

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(
            f"{ctx.command.name} was successfully invoked by {ctx.author} {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
        )

    @commands.command(name="henwee",
                      aliases=["henw"],
                      brief=henwees[random.randrange(0, len(henwees))])
    @cooldown(20, 30, BucketType.guild)
    async def henw(self, ctx):
        await ctx.send(henwees[random.randrange(0, len(henwees))],
                       file=discord.File("images/processed/henwee_fall.gif"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(
            f"{member} joined {member.guild} - ({member.id} joined {member.guild.id})"
        )
        if member.bot:
            return
        
        if member.guild.id == 694107776015663146:  # space
            await self.bot.get_channel(694197942000680980).send(
                f"Welcome, {member.mention}! Read through the <#694112817611276348>, assign yourself roles in <#925393973755908136>. And if you wish, introduce yourself in <#694192946387353680>"
            )
            await member.add_roles(
                member.guild.get_role(
                    694108297086631946
                )  #member.guild.get_role(766054606009794580)
            )

            try:
                await member.send(
                    f"Welcome to ***s p a c e !*** We hope you enjoy your stay :)"
                )

            except Forbidden:
                pass

        elif member.guild.id == 918787074801401868:  # frog
            await self.bot.get_channel(918787075434762242).send(
                f"YOOOOO {member.mention} JUST JOINED THE FROG AGENDAAAA!!!!")

        elif member.guild.id == 946136828916944987:  # constaleighton
            await self.bot.get_channel(946146531805900811).send(
                f"hello {member.mention}, have you wishlisted beaver clicker yet?\nhttps://store.steampowered.com/app/1718240"
            )

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "!" in ctx.content: return

        
        if random.randint(0,750) == 2: await react_beaver(ctx)
            
        try:
            hendex = random.randrange(0, len(henwees))
            if ctx.author.id == 192326730948542464:
                if random.randrange(0, 20) == 7:
                    await ctx.delete()

            log_ids = 411536312961597440
            if ctx.author.id == log_ids:
                with open("data/all_message_ids.json", "r") as f:
                    file = json.load(f)
                
                file[str(log_ids)]["messages"].append(ctx.id)
                
                with open("data/all_message_ids.json", "w") as f:
                    json.dump(file, f)


            listies = ["revaeb", "beavy", "dam", "damn", "beav", "bippa", "biba", "bev"] # if message ==
            listies2 = ["dam ", "bidoof", "beaver", "logs", "clicker"] # if in the message
            for x in range(0, len(listies)):
                if ctx.content.lower() == listies[x]:
                    await react_beaver(ctx)
            
            for x in range(0, len(listies2)):
                if listies2[x] in ctx.content.lower():
                    await react_beaver(ctx)

            if "b" in ctx.content and "e" in ctx.content and "a" in ctx.content and "v" in ctx.content and "r" in ctx.content and "c" in ctx.content and "l" in ctx.content and "i" in ctx.content and "c" in ctx.content and "k" in ctx.content and "o" in ctx.content and "n" in ctx.content and "s" in ctx.content and "t" in ctx.content and "m" in ctx.content:
                if random.randint(0, 50) == 2:
                    await ctx.add_reaction("<a:Beaver:950775158552014928>")

            if ("henwee" in ctx.content.lower() or "henw " in ctx.content.lower() or "411536312961597440" in ctx.content):# and ctx.author.id != self.bot.user.id:
                await ctx.add_reaction("<a:henwee_fall:955830194902544415>")
                await ctx.add_reaction(
                    "<a:henwee_fall_short:955878859197280306>")
                if random.randint(0, 5) == 2:
                    await ctx.add_reaction("<a:Beaver:950775158552014928>")
                if random.randrange(1, 9) == 2:  #1/8 chance
                    await ctx.channel.send(
                        henwees[hendex],
                        file=discord.File("images/processed/henwee_fall.gif"))

            elif "wee" in ctx.content and ctx.author != self.bot.user and (
                    ctx.guild.id == 926467601540993064
                    or ctx.guild.id == 918787074801401868
                    or ctx.guild.id == 694107776015663146):
                if random.randrange(1, 30) == 2:  #1/30
                    await ctx.channel.send(
                        henwees[hendex],
                        file=discord.File("images/processed/henwee_fall.gif"))

            elif "we" in ctx.content and ctx.author != self.bot.user and (
                    ctx.guild.id == 926467601540993064
                    or ctx.guild.id == 918787074801401868
                    or ctx.guild.id == 694107776015663146):
                if random.randrange(1, 150) == 2:  #1/150
                    await ctx.channel.send(
                        "you forgot an \"e\" at the end of you we there, it's fine though don't worry\n"
                        + henwees[hendex],
                        file=discord.File("images/processed/henwee_fall.gif"))
            
            if "sus" in ctx.content:
                    await ctx.reply("amogus")
            
            if "avengers assemble" in ctx.content:
                try:
                    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("avengers assemble", tenor_api_key, 10))

                    if r.status_code == 200:
                            top_x_gifs = json.loads(r.content)
                            realoutput = top_x_gifs['results'][random.randrange(0, 10)]['media'][0]["gif"]["url"]
                            
                            await ctx.send(realoutput)
                except Exception as e:
                    await ctx.send(e)
                    
            
            if "brain fuck" in ctx.content:
                    await ctx.add_reaction("🧠")
                    await ctx.add_reaction("🔫")
            

        except:
            pass

    @tasks.loop(seconds=293)
    async def henwee(self):
        if random.randrange(1, 7000) == 2:
            await self.bot.get_channel(919666600955760702).send(
                "reminder to keep on henweeing :)",
                file=discord.File("images/processed/henwee_fall.gif"))
    
    
    @tasks.loop(hours=1)
    async def random_beaver(self):
        if random.randrange(1, 400) == 2:
            members = []
            for guild in self.bot.guilds:
                for member in guild.members:
                    if member not in members:
                        members.append(member)

            lucky_winner = members[random.randint(0, len(members)-1)]
            
            try:
                i = self.bot.get_user(102862012689690624)
                await i.send("<a:Beaver:950775158552014928>")
                
                await lucky_winner.send(":Beaver: ")
                return lucky_winner.id
            except:
                await lucky_beaver(self)


async def lucky_beaver(self):
    members = []
    for guild in self.bot.guilds:
        for member in guild.members:
            if member not in members:
                members.append(member)

    lucky_winner = members[random.randint(0, len(members)-1)]
    try:
        await lucky_winner.send(":Beaver: ")
        return lucky_winner.id
    except:
        await lucky_beaver()


async def react_beaver(ctx):
    await ctx.add_reaction("<a:Beaver:950775158552014928>")
    if random.randrange(0, 40) == 2 and "beaver" in ctx.content:
        message = [
            "DID SOMEONE JUST SAY BEAVER?", "beav :)",
            "beaver clicker my beloved <3",
            "wishlist beaver clicker today!",
            "have you wishlisted beaver clicker yet?",
            "go ahead, wishlist beaver clicker already"
        ]
        index = random.randrange(0, 6)
        await ctx.channel.send(
            f"{message[index]}\nhttps://store.steampowered.com/app/1718240/Beaver_Clicker/"
        )

def setup(bot):
    bot.add_cog(events(bot))
