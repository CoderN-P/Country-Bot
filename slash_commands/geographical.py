import discord
from discord.ext import commands
import country_converter as coco
import random
import re
from fuzzywuzzy import fuzz
from countryinfo import CountryInfo
import datetime
from discord_slash import cog_ext

cc = coco.CountryConverter()
from main import country_filter


class GeographicalInfo2(
    commands.Cog,
    name="Geographical Info (slash)",
    description="Commands that give you geographical information about a country",
):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Check the area of a real country in sg. km.")
    async def area(self, ctx, *, country: str):
        data = await country_filter(country, ctx)
        if data is None:
            return
        result = data["area"]
        result2 = result / 1.609
        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        result2 = round(result2)
        embed = discord.Embed(
            title=f"Area of {country} — {alpha2} | {alpha3}",
            description="**The area of {country} is:\n `{result:,} sq. km` / `{result2:,} sq. mi`**".format(
                result=result, country=country, result2=result2
            ),
            color=0xFF5733,
        )

        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description="Check the region that a country is located in. (Must be a real country)"
    )
    async def region(self, ctx, *, country: str):
        data = await country_filter(country, ctx)
        if data is None:
            return
        result = data["region"]
        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        embed = discord.Embed(
            title=f"Region of {country} — {alpha2} | {alpha3}",
            description="**{country} is located in the region of `{result}`**".format(
                result=result, country=country
            ),
            color=0xFF5733,
        )

        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description="Check the subregion that a country is located in. (Must be a real country)"
    )
    async def subregion(self, ctx, *, country: str):
        data = await country_filter(country, ctx)
        if data is None:
            return
        result = data["subregion"]
        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        embed = discord.Embed(
            title=f"Subregion of {country} — {alpha2} | {alpha3}",
            description="**{country} is located in the subregion of `{result}`**".format(
                result=result, country=country
            ),
            color=0xFF5733,
        )

        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Get all the bordering countries of a real country.")
    async def borders(self, ctx, *, country: str):
        data = await country_filter(country, ctx)
        if data is None:
            return
        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        result = data["borders"]
        if len(result) == 0:
            await ctx.send(
                embed=discord.Embed(
                    title="Hmm",
                    description=f"{country} does not border any other countries",
                )
            )
            return
        string = ""
        result = coco.convert(names=result, to="name_short")
        if isinstance(result, str):
            string = f"`{result}`"
        else:
            for i in result:
                string += f"`{i}` "

        embed = discord.Embed(
            title=f"Borders of {country} — {alpha2} | {alpha3}",
            description="**{string}**".format(string=string),
            color=0xFF5733,
        )

        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Get all the timezones located in a real country.")
    async def timezone(self, ctx, *, country: str):
        data = await country_filter(country, ctx)
        if data is None:
            return
        result = data["timezones"]
        string = ""
        for i in result:
            string += f"`{i}` "
        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        embed = discord.Embed(
            title=f"Timezones of {country} — {alpha2} | {alpha3}",
            description="**{string}**".format(string=string),
            color=0xFF5733,
        )

        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Get the rough coordinates of a real country.")
    async def coords(self, ctx, *, country: str):
        data = await country_filter(country, ctx)
        if data is None:
            return
        result = data["latlng"]
        string = f"`{result[0]}, {result[1]}`"

        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        embed = discord.Embed(
            title=f"Approximate coordinates of {country} — {alpha2} | {alpha3}",
            description="**{string}**".format(string=string),
            color=0xFF5733,
        )

        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GeographicalInfo2(bot))
