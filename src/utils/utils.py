from disnake import Embed, Member, Colour

color = Colour.blue()

async def emb(ctx, message, user = None, colorarg = None, **kwargs):
    user = user or ctx.author
    emb = Embed(
        description = message,
        color = colorarg or color,
    ).set_footer(text = f"{user}", icon_url = user.avatar.url)
    return await ctx.send(embed = emb)


async def sendOverlay(ctx, endpoint, params: dict, user: Member):
    user = user or ctx.author
    prms = ""
    for _i, v in enumerate(params):
        if len(params) > 0:
            prms += f"{'?' if _i == 0 else '&'}{v}={params[v].replace(' ', '+')}"
    url = f"https://some-random-api.ml{endpoint}{prms}"
    await ctx.send(
        embed = Embed(color = color).set_author(name = user, icon_url = user.avatar.url).set_image(url = url))