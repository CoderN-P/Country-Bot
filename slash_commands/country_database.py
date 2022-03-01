from discord.ext import commands
import discord
import pycountry
import re
import datetime
from discord_slash import cog_ext


class CountryDatabase2(
    commands.Cog,
    name="Country Database (slash)",
    description="Commands that allow you to find countries!",
):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        description="List all countries in the world that start with the letter or letters that you provided."
    )
    async def list(self, ctx, letters: str):
        arg = letters
        check = arg
        new_list = []

        for x in pycountry.countries:
            s = x.name
            if re.match(check, s, re.I):
                new_list.append(x.name)

        for i, x in enumerate(new_list):
            new_list[i] = "`" + x + "`"
        result1 = " |".join(new_list)

        result2 = re.sub(r"(?<=[|])(?=[^\s])", r" ", result1)

        if not result2:
            embed = discord.Embed(
                title="Sorry",
                description="**there are no countries starting with {}**".format(arg),
                color=0xFF5733,
            )

            embed.set_thumbnail(
                url="https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg"
            )

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Countries starting with " + arg,
                description="**{result2}**".format(result2=result2),
                color=0xFF5733,
            )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CountryDatabase2(bot))
