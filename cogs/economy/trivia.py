import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import html
import random
import requests


from libraries.economyLib import *
from libraries.miscLib import get_input
from libraries.settings import *


class ecotrivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="trivia",
        aliases=["quiz", "triv"],
        brief=f"""
        play trivia with your friends!
        valid difficulty levels are: easy, medium, hard, or e, m, h
        for a list of categories, use a!trivia categories or a!trivia help
        """,
    )
    @cooldown(1, 2, BucketType.user)
    async def triviaCommand(self, ctx, category="random", difficulty="random"):
        dif = difficulty
        await ctx.channel.typing()
        help_strs = ["help", "category", "categories"]
        if category.lower() in help_strs:
            await ctx.send(
                f"""
List of valid categories, to play a specific category, use the category name or ID {ctx.prefix}trivia <category> <difficulty>
if you want to add more questions to the database, go to <https://opentdb.com/>, create a new account, and add your questions there

General - ID = 1
Books - ID = 2
Film - ID = 3
Music - ID = 4
Musicals & Theatres - ID = 5
Television - ID = 6
Video Games - ID = 7
Board Games - ID = 8
Science & Nature - ID = 9
Computers - ID = 10
Mathematics - ID = 11
Mythology - ID = 12
Sports - ID = 13
Geography - ID = 14
History - ID = 15
Politics - ID = 16
Art - ID = 17
Celebrities - ID = 18
Animals - ID = 19
Vehicles - ID = 20
Comics - ID = 21
Gadgets - ID = 22
Japanese Anime & Manga - ID = 23
Cartoon & Animations - ID = 24
Beavers - ID = 25 (does not have difficulties)

            """
            )
            return

        # THIS IS LITTERALLY JUST A COPY OF THE CODE BUT SLIGHTLY MODIFIED AS IT USES A COMPLETELY DIFFERENT API, aka a fucking json file lmao
        if str(category).lower() in ["beav", "beaver", "beavers", "25"]:
            with open("storage/misc/beaver_quiz.json", "r") as f:
                quiz_data = json.load(f)

            question = quiz_data[f"question{random.randrange(0, len(quiz_data))}"]

            answers = [question["correct"], question["ans0"], question["ans1"], question["ans2"]]

            random.shuffle(answers)

            abcd = ["a", "b", "c", "d"]

            for abc, answer in zip(abcd, answers):
                if answer == question["correct"]:
                    correct_answer_ID = abc
                    correct_answer = answer
                    break

            embed = discord.Embed(title="Trivia", description=f"**Beavers || ID: 25**", color=ctx.author.color)
            embed.add_field(name="Question", value=question["title"], inline=False)
            embed.add_field(
                name="is it?",
                value=f"""
a) {answers[0]}
b) {answers[1]}
c) {answers[2]}
d) {answers[3]}
                            """,
                inline=False,
            )

            await ctx.send(embed=embed)

            response = await get_input(self, ctx, 25)

            if response.content.lower() == correct_answer.lower() or response.content.lower() == correct_answer_ID:
                await ctx.send(f"{ctx.author.mention} you are correct! it was {correct_answer_ID}, {correct_answer}")
                return

            await ctx.send(f"sorry, the answer was {correct_answer_ID}, {correct_answer}")
            return

        # if category is not beaver, continue as normal

        req_str = "https://opentdb.com/api.php?amount=1"

        difs = ["easy", "medium", "hard"]
        short_difs = ["e", "m", "h"]

        for x, y in zip(difs, short_difs):
            if category.lower() == x.lower() or category.lower() == y.lower():
                req_str += f"&difficulty={x}"
                category = "random"
                break

        for x, y in zip(difs, short_difs):
            if dif.lower() == x.lower() or dif.lower() == y.lower():
                req_str += f"&difficulty={x}"
                break

        human_readable_categories = [
            "General",
            "Books",
            "Film",
            "Music",
            "Musicals & Theatres",
            "Television",
            "Video Games",
            "Board Games",
            "Science & Nature",
            "Computers",
            "Mathematics",
            "Mythology",
            "Sports",
            "Geography",
            "History",
            "Politics",
            "Art",
            "Celebrities",
            "Animals",
            "Vehicles",
            "Comics",
            "Gadgets",
            "Japanese Anime & Manga",
            "Cartoon & Animations",
        ]
        categories = [
            "General Knowledge",
            "Entertainment: Books",
            "Entertainment: Film",
            "Entertainment: Music",
            "Entertainment: Musicals & Theatres",
            "Entertainment: Television",
            "Entertainment: Video Games",
            "Entertainment: Board Games",
            "Science & Nature",
            "Science: Computers",
            "Science: Mathematics",
            "Mythology",
            "Sports",
            "Geography",
            "History",
            "Politics",
            "Art",
            "Celebrities",
            "Animals",
            "Vehicles",
            "Entertainment: Comics",
            "Science: Gadgets",
            "Entertainment: Japanese Anime & Manga",
            "Entertainment: Cartoon & Animations",
        ]
        category_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        random_categories = ["random", "rand", "r", "any", "a", "all"]

        if category.lower() not in random_categories:
            for z, x, y in zip(human_readable_categories, categories, category_ids):
                if category.lower() == z.lower() or category.lower() == x.lower() or category.lower() == str(y):
                    req_str += f"&category={y+8}"
                    break

        r = requests.get(f"{req_str}&type=multiple")

        questions = json.loads(r.content)
        if questions["response_code"] != 0:
            if questions["response_code"] == 1:
                return await ctx.send("**Code 1: No Results** Could not return results. The API doesn't have enough questions for your query.")
            if questions["response_code"] == 2:
                return await ctx.send("**Code 2: Invalid Parameter** Contains an invalid parameter. Arguements passed in aren't valid.")
            if questions["response_code"] == 3:
                return await ctx.send("**Code 3: Token Not Found** Session Token does not exist.")
            if questions["response_code"] == 4:
                return await ctx.send(
                    "**Code 4: Token Empty** Session Token has returned all possible questions for the specified query. Resetting the Token is necessary."
                )

            return await ctx.send(f"error code {questions['response_code']}, please try again later")

        questions = questions["results"][0]
        answers = [
            html.unescape(questions["correct_answer"]),
            html.unescape(questions["incorrect_answers"][0]),
            html.unescape(questions["incorrect_answers"][1]),
            html.unescape(questions["incorrect_answers"][2]),
        ]

        random.shuffle(answers)

        abcd = ["a", "b", "c", "d"]

        for abc, answer in zip(abcd, answers):
            if answer == html.unescape(questions["correct_answer"]):
                correct = abc
                break

        result_category_id = "None"
        reslult_category = questions["category"]
        for x, y in zip(categories, category_ids):
            if x == reslult_category:
                result_category_id = y
                break

        embed = discord.Embed(title="Trivia", description=f"**{reslult_category} || ID: {result_category_id}**", color=ctx.author.color)
        embed.set_footer(text=f"Difficulty: {questions['difficulty']}")

        embed.add_field(name="Question:", value=f"{html.unescape(questions['question'])}", inline=False)
        embed.add_field(
            name="is it?",
            value=f"""
a) {answers[0]}
b) {answers[1]}
c) {answers[2]}
d) {answers[3]}
                        """,
            inline=False,
        )

        await ctx.send(embed=embed)

        response = await get_input(self, ctx, 25)

        if response.content.lower() == questions["correct_answer"].lower() or response.content.lower() == correct:
            await ctx.send(f"{ctx.author.mention} you are correct! it was {correct}, {html.unescape(questions['correct_answer'])}")
            return

        await ctx.send(f"sorry, the answer was {correct}, {html.unescape(questions['correct_answer'])}")


async def setup(bot):
    await bot.add_cog(ecotrivia(bot))
