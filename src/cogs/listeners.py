import json

from disnake.ext.commands import Cog, command
from disnake import Message

class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_delete(self, msg: Message) -> None:
        bannedWords = ['faggot', 'fag', 'fagg', 'f*ggot', 'nigga', 'nigger', 'n*gga', 'n*gger', 'discord.gg/invite', '/invite', 'https:']
        for i in bannedWords:
            if i in msg.content: return
        with open("src/dicts/snipe.json", "r") as f:
            load = json.load(f)
        load.append(
            {
                "author": msg.author.id,
                "message": msg.content,
                "reference": msg.reference.message_id if msg.reference != None else None
            }
        )
        with open("src/dicts/snipe.json", "w") as f:
            json.dump(load, f)

def setup(bot):
    bot.add_cog(Listeners(bot))