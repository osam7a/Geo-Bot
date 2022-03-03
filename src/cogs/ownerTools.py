import disnake.ext.commands
from disnake.ext.commands import Cog, command, is_owner, ExtensionNotLoaded
from ..utils.eval import run_eval
from ..utils.utils import emb

class OwnerTools(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @is_owner()
    async def eval(self, ctx, *, code):
        b = code.lstrip("```py")
        a = b.rstrip("```")
        x = await run_eval(ctx, a)
        try:
            await ctx.send(x)
        except:
            pass

    @command()
    @is_owner()
    async def reload(self, ctx, cog):
        try:
            self.bot.unload_extension(f"src.cogs.{cog}")
            self.bot.load_extension(f"src.cogs.{cog}")
            await emb(ctx, "Reloaded extension")
        except ExtensionNotLoaded:
            self.bot.load_extension(f"src.cogs.{cog}")
            await emb(ctx, "Extension loaded")

def setup(bot):
    bot.add_cog(OwnerTools(bot))