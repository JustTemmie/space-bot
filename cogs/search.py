import discord
from discord import Member, File, Embed, Intents, Object, NotFound
from discord.errors import HTTPException, Forbidden
from discord.ext import tasks, commands

# from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import (
    cooldown,
    BucketType,
    MissingRequiredArgument,
)

import requests
import wikipedia
import urllib
import re
import random
import imdb

import libraries.standardLib as SL

class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="urban",
        aliases=["what", "meaning"],
        brief="search up something using urban dictionary",
    )
    @cooldown(5, 20, BucketType.user)
    async def urbandictionary(self, ctx, *, search):
        if not ctx.channel.is_nsfw():
            return await ctx.send("this command is sadly for NSFW channels only for now, sorry")
        
        await ctx.trigger_typing()
        req = requests.get(
            "http://api.urbandictionary.com/v0/define?term=" + urllib.parse.quote(search)
        )
        if req.status_code == 404:
            await ctx.send("No urban dictionary entry found for " + (await SL.removeat(search)))
            return

        entry = 0
        embed = discord.Embed(
            title=search.title(),
            description=req.json()["list"][entry]["definition"],
            colour=ctx.author.colour,            
        )
        #embed.set_footer(text=f"page {entry+1} of {len(req.json()['list'])}")
        embed.add_field(name="Example", value=req.json()["list"][entry]["example"])
        msg = await ctx.send(embed=embed)
        
        

    
    async def check_nsfw(self, ctx, json, loops = 0):
        if loops > 5:
            return False
        
        req_len = len(json["data"]["children"])
        rand = random.randrange(0, req_len)
        post = json["data"]["children"][rand]
        
        if post["data"]["over_18"] and not ctx.channel.is_nsfw():
            return await self.check_nsfw(ctx, json, loops + 1)
        
        return post
    
    @commands.command(
        name="imdb",
        brief="search up a movie using imdb",
    )
    @cooldown(5, 20, BucketType.user)
    async def imdb_command(self, ctx, *, movie):

        try:
            movie = imdb.IMDb().search_movie(movie)
            title = movie[0]["title"]
            movieObj = imdb.IMDb().get_movie(movie[0].getID())

            rateStr = "★" * round(movieObj["rating"])
            while len(rateStr) < 10:
                rateStr += "☆"
            rateStr += f" ({movieObj['rating']}/10)"

            dict = {
                "Plot": movieObj["plot"][0],
                "Genres": ", ".join(movieObj["genres"]),
                "Rating": rateStr,
                "Cast" : ", ".join([str(x) for x in movieObj["cast"]][:5]),
                "Writer": ", ".join([str(x) for x in movieObj["writer"]]),
                "Year" : movieObj["year"]
            }

            embed = Embed(
                title=movieObj["title"],
                color=ctx.author.colour
            )

            for i in dict:
                embed.add_field(name=i, value=dict[i], inline=False)
  
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.send(f"Error: {e}")

    
    @commands.command(
        name="reddit",
        aliases=["red", "r/", "rslash", "r"],
        brief="get a random reddit post from the specified subreddit",
    )
    @cooldown(1, 2, BucketType.guild)
    async def reddit_search(self, ctx, *, search):
        if search == "tra" or search == "traa":
            search = "traaaaaaannnnnnnnnns"
        
        req = requests.get(
            "http://reddit.com/r/" + search + "/hot/.json?limit=50",
            headers={"User-agent": "Chrome"},
        )
        json = req.json()
        if "error" in json or json["data"]["after"] is None:
            await ctx.send('Subreddit "{}" not found'.format(search), delete_after=(15))
            return
        
        post = await self.check_nsfw(ctx, json)
        if not post:
            return await ctx.send(f"Could not find a post in {search} that wasn't NSFW", delete_after=(15))
        

        title = post["data"]["title"]
        author = "u/" + post["data"]["author"]
        subreddit = post["data"]["subreddit_name_prefixed"]
        url = post["data"]["url"]  # can be image or post link
        link = "https://reddit.com" + post["data"]["permalink"]
        if "selftext" in post["data"]:
            text = post["data"]["selftext"]  # may not exist
            if len(text) >= 2000:
                text = text[:2000].rsplit(" ", 1)[0] + " **-Snippet-**"
            embed = discord.Embed(title=title, description=text, url=link)
        else:
            embed = discord.Embed(title=title, url=link)

        if re.match(r".*\.(jpg|png|gif)$", url):
            embed.set_image(url=url)

        embed.set_footer(text="By {} in {}".format(author, subreddit))

        await ctx.send(embed=embed)

    @commands.command(
        name="youtube",
        aliases=["yt", "youtubesearch", "ytsearch"],
        brief='Responds with a link containing the search keywords given by the user, or if the input starts with "channel" or "user" it redirects to the account with that custom url, if it exists',
    )
    @cooldown(20, 300, BucketType.user)
    async def youtube_search(self, ctx, *, input=None):
        link = "https://www.youtube.com/results?search_query=" + (str(input))
        channel_link = "https://www.youtube.com/user/"

        if input == None:
            link = "https://youtube.com"
            await ctx.send(f"no input was given, redirected to youtube.com instead\n{link}")

        elif input.startswith("channel") or input.startswith("user"):
            if input.startswith("channel"):
                newinput = input[8:]
            else:
                newinput = input[5:]
            await ctx.send(
                f'tried finding the user "{newinput}"\n'
                + channel_link
                + (str(newinput)).replace(" ", "+")
            )

        elif input != None:
            await ctx.send(f'search results for "{input}"\n' + link.replace(" ", "+"))

    @commands.command(
        name="wikipedia",
        aliases=["wiki"],
        brief="Find a Wikipedia page on a given topic - does not work on all pages as some may be too short, sorry - note - this uses wikipedia.org so it's only capable to search up questions on the english page, not other languages",
    )
    @cooldown(3, 10, BucketType.guild)
    async def wikipedia_search(self, ctx, *, search):
        if not ctx.channel.is_nsfw():
            return await ctx.send("this command is sadly for NSFW channels only for now, sorry")
                                  
        await ctx.channel.trigger_typing()
        search = wikipedia.search(search)

        if not search:
            await ctx.send("No page was found for the search term" + (search))
            return

        page = wikipedia.page(search[0])
        title = page.title
        body = page.summary
        if len(body) >= 2000:
            body = body[:2000].rsplit(" ", 1)[0] + " **-Snippet-**"
        image = page.images[0]
        url = page.url

        embed = discord.Embed(title=title, description=body, url=url)
        embed.set_footer(text="From Wikipedia")
        embed.set_thumbnail(url=image)

        await ctx.send(embed=embed)

    @commands.command(
        name="minecraftchampionship",
        aliases=["mcc", "linkmcc"],
        brief="links the mcc page of the week",
    )
    @cooldown(2, 120, BucketType.guild)
    async def mcc(self, ctx):
        await ctx.send("https://mcc.live/")


def setup(bot):
    bot.add_cog(search(bot))
