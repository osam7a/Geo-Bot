import base64
import json

import aiohttp
import random
import asyncio

from disnake.ext.commands import Cog, command
from disnake import Embed, Color, Member
from art import text2art

from ..utils.utils import emb, color, get


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    @staticmethod
    def scrambled(orig):
        dest = orig[:]
        random.shuffle(dest)
        return dest

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
        await ctx.reply(embed = embz)
        chosen = await self.bot.wait_for('message',
                                         check = lambda m: m.author == ctx.author and ctx.channel == m.channel,
                                         timeout = 30)
        try:
            chosen = _categsNums[chosen.content]
        except KeyError:
            return await emb(ctx, "Invalid choice!", color = Color.red())
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
                for _i, v in enumerate(self.scrambled(choices)):
                    choicesStr += f"**{_i + 1}.** {v}\n"
                    chDict[_i + 1] = v
                await ctx.reply(embed = Embed(
                    title = questionStr,
                    description = choicesStr,
                    color = color
                ))
                choiceM = await self.bot.wait_for('message',
                                                 check = lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                                 timeout = 60)
                choice = choiceM.content
                try:
                    _temp = chDict[int(choice)]
                except:
                    choice = "cancel"
                while chDict[int(choice)] != correctAnswer and choice != "cancel":
                    await choiceM.reply(f"You chose {chDict[int(choice)]}, Incorrect! Type \"cancel\" to cancel")
                    choiceM = await self.bot.wait_for('message', check = lambda
                        m: m.author == ctx.author and m.channel == ctx.channel)
                    choice = choiceM.content
                    if choice == "cancel": return await choiceM.reply("Cancelled.")
                await choiceM.reply(f"You chose {chDict[int(choice)]}, won!")

    @command()
    async def fact(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://uselessfacts.jsph.pl/random.json?language=en") as resp:
                _json = await resp.json()
                fact = _json['text']
                await ctx.send(f"**{fact}**")

    @command()
    async def yomama(self, ctx, *, user: Member = None):
        user = user or ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://yomomma-api.herokuapp.com/jokes") as res:
                _json = await res.json()
                joke = _json['joke']
                await ctx.send(f"{user.mention} {joke}")

    @command()
    async def quote(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://inspiration.goprogram.ai/") as res:
                _json = await res.json()
                await ctx.send(f"\"{_json['quote']}\" - {_json['author']}")

    @command(aliases = ['ascii', 'text2art'])
    async def textart(self, ctx, *, message):
        if len(message) > 13:
            return await ctx.reply("Message too long")
        ref = ctx.message.reference
        try:
            msg = self.bot.get_message(ref.message_id)
            await msg.reply(
                f"```\n{'shortened text (less than 15)' if len(message) > 15 else ''}\n{text2art(message if len(message) < 15 else message[:15])}\n```")
        except:
            await ctx.reply(
                f"```\n{'shortened text (less than 15)' if len(message) > 15 else ''}\n{text2art(message if len(message) < 15 else message[:15])}\n```")

    @command()
    async def snipe(self, ctx):
        with open("src/dicts/snipe.json") as f:
            load = json.load(f)
            if len(load) == 0:
                return await emb(ctx, "No one ever deleted a message at this moment!", color = Color.red())
            lastMsg = load[-1]
            result = ""
            author = await self.bot.fetch_user(lastMsg['author'])
            if lastMsg['reference'] != None:
                msg = self.bot.get_message(lastMsg['reference'])
                if msg != None:
                   result += f"{author} replying to {msg.author.mention} \"{msg.content}\": \n{lastMsg['message']}"
                else: result += f"{author}: {lastMsg['message']}"

            else:
                result += f"{author}: {lastMsg['message']}"
            await emb(ctx, result)
    @command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/{random.choice(['memes', 'dankmemes', 'wholesomememes', 'historymemes', 'geographymemes', 'antimeme'])}.json?nsfw=false") as resp:
                _json = await resp.json()
                randomPost = random.choice(_json['data']['children'])['data']
                title = randomPost['title']
                postLink = "https://reddit.com" + randomPost['permalink']
                try:
                    imageUrl = randomPost['url_overridden_by_dest']
                except: imageUrl = 'https://st4.depositphotos.com/14953852/24787/v/600/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg'
                footer = f"Author: {randomPost['author']} this post had {randomPost['ups']} upvotes and {randomPost['downs']} downvotes"
                await ctx.send(embed = Embed(
                    title = title, url = postLink,
                    color = color
                ).set_image(
                    url = imageUrl
                ).set_footer(
                    text = footer
                ))

    @command()
    async def binary(self, ctx, encodeordecode, *, message):
        if encodeordecode.lower() == "encode":
            result = get('sra', '/binary', { "encode": message }).json()['binary']
        elif encodeordecode.lower() == "decode":
            result = get('sra', '/binary', { "decode": message }).json()['text']
        return await emb(ctx, f"```\n{result}\n```")

    @command()
    async def roast(self, ctx, *, user: Member = None):
        user = user or ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://evilinsult.com/generate_insult.php?lang=en&type=json") as resp:
                _json = await resp.json()
                return await emb(ctx, _json['insult'])

    @command()
    async def hack(self, ctx, *, user: Member = None):
        user = user or ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://randomuser.me/api/", headers = { "Content-Type": "application/json" }) as resp:
                _user = await resp.json()
                _user = _user['results'][0]
            async with cs.get("https://www.themealdb.com/api/json/v1/1/random.php") as resp:
                _food = await resp.json()
                _food = _food['meals'][0]

        nouns = ["bird", "clock", "boy", "plastic", "duck", "teacher", "old lady", "professor", "hamster", "dog"];
        verbs = ["kicked", "ran", "flew", "dodged", "sliced", "rolled", "died", "breathed", "slept", "killed"];
        adjectives = ["beautiful", "lazy", "professional", "lovely", "dumb", "rough", "soft", "hot", "vibrating",
                      "slimy"];
        adverbs = ["slowly", "elegantly", "precisely", "quickly", "sadly", "humbly", "proudly", "shockingly", "calmly",
                   "passionately"];
        preposition = ["down", "into", "up", "on", "upon", "below", "above", "through", "across", "towards"]

        sentence = f"The {random.choice(adjectives)} {random.choice(nouns)} {random.choice(adverbs)} {random.choice(verbs)} {random.choice(preposition)} the {random.choice(nouns)}"
        name = _user['name']['first'] + " " + _user['name']['last']
        sentences = {
            "Name: ": name,
            "Instagram User: ": _user['login']['username'],
            "Instagram Password: ": _user['login']['password'],
            "Phone Number: ": _user['phone'],
            "Age: ": _user['dob']['age'],
            "Finding Country.... ": _user['location']['country'],
            "Likes turtles? ": random.choice(['Yes', 'No']),
            "Broken Table? ": random.choice(['Yes', 'No']),
            f"`{user}.fetch_last_dm()` ": sentence,
            "Favorite food: ": _food['strMeal'],
            f"`{user}.is_racist()` ": random.choice(['Yes', 'No']),
            "is hot? ": random.choice(['Yes', 'No']),
            "Gay? ": random.choice(['Yes', 'No']),
            "Favorite Sport: ": random.choice(['football', 'soccer', 'basketball', 'volleyball', 'tennis'])
        }

        msg = await emb(ctx, f"Hacking {user.mention}...")
        await asyncio.sleep(1.5)
        for k, v in sentences.items():
            await msg.edit(embed = Embed(title = f"{k}", color = color))
            await asyncio.sleep(1.5)
            await msg.edit(embed = Embed(title = f"{k}", description = v, color = color))
            await asyncio.sleep(1.5)
        await msg.edit(content = f"The totally real hack just finished...")
def setup(bot):
    bot.add_cog(Fun(bot))