import json

from disnake.ext.commands import Cog, command
from disnake import Message

from ..utils.utils import emb
from ..utils.db import Database
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

    @Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.content in [f'<@{self.bot.user.id}>', f'<@!{self.bot.user.id}>']:
            async with Database("users.db", "users", "(id INTEGER, warns INTEGER, prefix TEXT)") as db:
                mem = await db.getMember(msg.author.id)
                prefix = await mem.prefix
            await emb(msg.channel, f"```yaml\nDefault prefix: \"geo \"\nYour prefix: {prefix}\n```\nExample usage:\n```\n{prefix}help\n```", user = msg.author)
def setup(bot):
    bot.add_cog(Listeners(bot))