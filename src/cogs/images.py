from inspect import Parameter
from typing import Union
from disnake import Member
from disnake.ext.commands import Cog, command, MissingRequiredArgument
from ..utils.utils import emb, sendOverlay
from disnake.utils import find


class Images(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def gay(self, ctx, *, user: Member = None):
        user = user or ctx.author
        await sendOverlay(ctx, "/canvas/gay", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def wasted(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/wasted", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def jail(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/jail", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def passed(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/passed", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def triggered(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/triggered", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def glass(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/glass", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def comrade(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/comrade", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def grayscale(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/greyscale", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def invert(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/invert", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def brightness(self, ctx, brightness: int, user: Member = None):
        user = user or ctx.author
        if brightness < 0 or brightness > 255:
            return await emb(ctx, f"Brightness should be between 0 - 255")
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/brightness",
                          { "avatar": user.avatar.with_format('png').url, "brightness": brightness }, user)

    @command(aliases = ['pixels', 'lowres', 'lowresolution'])
    async def pixelate(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/pixelate", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def blur(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/blur", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def simpcard(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/simpcard", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def lolice(self, ctx, *, user: Member = None):
        user = user or ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/lolice", { "avatar": user.avatar.with_format('png').url }, user)

    @command()
    async def youtube(self, ctx, user: Union[Member, str] = None, *, message = None):
        if not user and not message:
            raise MissingRequiredArgument(Parameter('user', Parameter.POSITIONAL_ONLY, default = None))
        elif user and not message:
            raise MissingRequiredArgument(Parameter('message', Parameter.POSITIONAL_ONLY, default = None))
        if isinstance(user, str):
            message = ctx.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:]
            user = ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/youtube-comment",
                          { "avatar": user.avatar.with_format('png').url, "username": user.display_name,
                            "comment": message }, user)

    @command()
    async def stupid(self, ctx, user: Union[Member, str] = None, *, message = None):
        if not user and not message:
            raise MissingRequiredArgument(Parameter('user', Parameter.POSITIONAL_ONLY, default = None))
        elif user and not message:
            raise MissingRequiredArgument(Parameter('message', Parameter.POSITIONAL_ONLY, default = None))
        if isinstance(user, str):
            message = ctx.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:]
            user = ctx.author
        if user.avatar == None:
            return await emb(ctx, f"{user.mention} Doesnt have an avatar...")
        await sendOverlay(ctx, "/canvas/its-so-stupid",
                          { "avatar": user.avatar.with_format('png').url, "dog": message }, user)


def setup(bot):
    bot.add_cog(Images(bot))