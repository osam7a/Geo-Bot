from src.utils.db import Database
from src.bot import GeoBot
from src.utils.HIDDEN import TOKEN

if __name__ == "__main__":
    async def getPrefix(self, msg):
        author = msg.author.id
        async with Database("users.db", "users", "(id INTEGER, warns INTEGER, prefix TEXT)") as db:
            mem = await db.getMember(author)
            return await mem.prefix
    GeoBot(getPrefix).run(TOKEN)