from discord.ext import commands
from bot_utils.country_filter import country_filter
import discord


@commands.command(
        brief="Get the general currency of a real country.",
        description="Get the general currency of a real country.",
)
async def currency(self, ctx, *, country):
    data = await country_filter(country, ctx)
    if data is None:
        return
    name = data["name"]
    alpha2 = data["alpha2Code"]
    alpha3 = data["alpha3Code"]
    string = ""
    for i in data["currencies"]:
        code = i["code"]
        name2 = i["name"]
        symbol = i["symbol"]
        string += f"```{code} {name2} {symbol}``` "

    embed = discord.Embed(
        title=f"Currency of {name} — {alpha2} | {alpha3}",
        description=string,
        color=0xFF5733,
    )
    embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

    embed.set_footer(
        text="Requested by: {name}".format(name=ctx.author),
        icon_url=ctx.author.avatar_url,
    )

    await ctx.send(embed=embed)