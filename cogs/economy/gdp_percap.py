from discord.ext import commands
import discord
from bot_utils.country_filter import country_filter
import country_converter as coco
import wbdata

cc = coco.CountryConverter()
url = "https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg"



@commands.command(
    brief="Get the gdp per capita of a real country in a certain year.",
    description="Get the gdp per capita of a real country in a certain year.",
)
async def gdp_percap(self, ctx, country, year):
    country = await country_filter(country, ctx)
    if country is None:
        return
    arg = country["name"]
    arg2 = year

    try:
        int(year)
    except:
        await ctx.send(":x: You did not enter a valid year!")
        return
    try:
        country1 = coco.convert(names=arg, to="iso2")
        country1 = country1.upper()
        country2 = []
        country2.append(country1)

        indicators = {"NY.GDP.PCAP.CD": "GDP per Capita"}

        # grab indicators above for countires above and load into data frame
        df = wbdata.get_dataframe(
            indicators, country=country2, convert_date=False
        ).to_dict()["GDP per Capita"][arg2]

        if str(df) == "nan":
            embed = discord.Embed(
                title="Sorry",
                description="**We couldn't find data for that year**".format(arg),
                color=0xFF5733,
            )

            embed.set_thumbnail(url=url)
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="GDP per capita of {}".format(arg),
                description=f"The gdp per capita of {arg} in {arg2} is/was $`{df}`",
                color=0xFF5733,
            )

            result3 = coco.convert(names=arg, to="ISO2")
            embed.set_thumbnail(
                url=f"https://flagcdn.com/w80/{result3.lower()}.jpg"
            )

            embed.set_footer(
                text="Information requested by: {}".format(ctx.message.author)
            )

            await ctx.channel.send(embed=embed)

    except:
        embed = discord.Embed(
            title="Sorry",
            description="** We could not find data for that year**",
            color=0xFF5733,
        )

        embed.set_thumbnail(url=url)

        await ctx.channel.send(embed=embed)
