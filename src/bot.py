import os
import traceback

from disnake.ext.commands import Bot
from .utils.logging import Log

class GeoBot(Bot):
    def __init__(self, prefix, **kwargs):
        super().__init__(command_prefix = prefix, **kwargs)
        self.log = Log("src/main.log", self)
        self.log.info("Bot initialized")
        print("Bot initialized")
        self.load_commands()

    def load_commands(self):
        @self.command()
        async def ping(ctx):
            return await ctx.send(f"Pong! `{round(self.latency * 1000)}ms`")

    async def on_ready(self):
        for i in os.listdir("src/cogs"):
            try:
                self.load_extension(f"src.cogs.{i}")
                self.log.info(f"Loaded {i}")
            except Exception as e:
                err = ''.join(traceback.format_exception(e, e, e.__traceback__))
                print(f"Cog {i} Failed, check errors log")
                await self.log.error(err)
        print("Cogs loaded successfully")
        self.log.info("Cogs loaded successfully")
        print(f"Latency: {round(self.latency * 1000)}ms")
        self.log.info(f"Latency: {round(self.latency * 1000)}ms")


