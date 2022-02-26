import base64
import aiohttp

from disnake.ext.commands import Cog, command
from disnake import Embed, Color

import src.utils.utils


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def trivia(self, ctx):
        await ctx.send("**Command in development, if you find any bugs, dm osam7a#1017**")
        categories = ""
        _categs = {
            "a) ": "General Knowledge",
            "b) ": "Books",
            "c) ": "Films",
            "d) ": "Music",
            "e) ": "Musicals & Theaters",
            "f) ": "TV (Television)",
            "g) ": "Video Games",
            "h) ": "Board Games",
            "i) ": "Science & Nature",
            "j) ": "Science: Computers",
            "k) ": "Science: Mathematics",
            "l) ": "Mythology",
            "m) ": "Sports",
            "n) ": "Geography",
            "o) ": "History",
            "p) ": "Politics",
            "q) ": "Art",
            "r) ": "Celebrities",
            "s) ": "Animals",
            "t) ": "Vehicles",
            "u) ": "Comics",
            "v) ": "Science: Gadgets",
            "w) ": "Anime",
            "x) ": "Cartoon & Animations"
        }
        _categsNums = {
            "a": 9,
            "b": 10,
            "c": 11,
            "d": 12,
            "e": 13,
            "f": 14,
            "g": 15,
            "h": 16,
            "i": 17,
            "j": 18,
            "k": 19,
            "l": 20,
            "m": 21,
            "n": 22,
            "o": 23,
            "p": 24,
            "q": 25,
            "r": 26,
            "s": 27,
            "t": 28,
            "u": 29,
            "v": 30,
            "w": 31,
            "x": 32
        }
        color = Color.blue()
        for k, v in _categs.items():
            categories += f"**{k}**{v}\n"
        embz = Embed(title = "Category list", description = categories, color = color).set_footer(
            text = "Reply with the letter matching the category you need... Example: `a)`")
        await ctx.send(embed = embz)
        chosen = await self.bot.wait_for('message',
                                         check = lambda m: m.author == ctx.author and ctx.channel == m.channel,
                                         timeout = 30)
        try:
            chosen = _categsNums[chosen.content]
        except KeyError:
            return await src.utils.utils.emb(ctx, "Invalid choice!", color = Color.red())
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    f"https://opentdb.com/api.php?amount=1&category={chosen}&difficulty=easy&encode=base64") as res:
                _json = await res.json()
                question = _json['results'][0]
                questionStr = base64.b64decode(question['question'].encode()).decode()
                correctAnswer = base64.b64decode(question['correct_answer'].encode()).decode()
                choices = [correctAnswer]
                for i in question['incorrect_answers']:
                    choices.append(base64.b64decode(i.encode()).decode())
                choicesStr = ""
                chDict = { }
                for _i, v in enumerate(choices):
                    choicesStr += f"**{_i + 1}.** {v}\n"
                    chDict[_i + 1] = v
                await ctx.send(embed = Embed(
                    title = questionStr,
                    description = choicesStr,
                    color = color
                ))
                choice = await self.bot.wait_for('message',
                                                 check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
                choice = choice.content
                try:
                    _temp = chDict[int(choice)]
                except:
                    choice = "cancel"
                while chDict[int(choice)] != correctAnswer and choice != "cancel":
                    await ctx.send(f"You chose {chDict[int(choice)]}, Incorrect! Type \"cancel\" to cancel")
                    choice = await self.bot.wait_for('message', check = lambda
                        m: m.author == ctx.author and m.channel == ctx.channel)
                    choice = choice.content
                    if choice == "cancel": return await ctx.send("Cancelled.")
                await ctx.send(f"You chose {chDict[int(choice)]}, won!")

def setup(bot):
    bot.add_cog(Fun(bot))