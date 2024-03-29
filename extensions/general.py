import discord
from discord.ext import commands
import country_converter as coco
import random
import re
import pycountry
from fuzzywuzzy import fuzz
from mongomethods import count
from countryinfo import CountryInfo
from discord import Color
import json
import requests
import datetime
import time
import resource
import psutil
import wikipedia
from main import country_filter

main_up = time.time()


quiz_country_list = list(CountryInfo().all().keys())


class General(
    commands.Cog,
    name="General Data",
    description="Commands that return general data about the bot, and real life countries",
):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="Look at the flag of a random real country or specify a certain country.",
        brief="Look at the flag of a random real country or specify a certain country.",
    )
    async def flag(self, ctx, *country: str):
        if len(country) == 0:
            country = random.choice(quiz_country_list)
            result4 = coco.convert(names=country, to="ISO2")
            url = f"https://flagcdn.com/w320/{result4.lower()}.jpg"
            e = discord.Embed(title=f"Flag of {country.title()}")
            e.set_image(url=url)
            await ctx.send(embed=e)
        else:
            country = " ".join(country)
            country = await country_filter(country, ctx)
            if country is None:
                return
            country = country["name"]
            result4 = coco.convert(names=country, to="ISO2")

            url = f"https://flagcdn.com/w320/{result4.lower()}.jpg"
            e = discord.Embed(title=f"Flag of {country.title()}")
            e.set_image(url=url)
            try:
                await ctx.send(embed=e)
            except:
                embed = discord.Embed(
                    title="Error", description=":x: Country not found"
                )
                await ctx.send(embed=embed)

    @commands.command(
        name="capital",
        description="Get the capital of a real country.",
        brief="Get the capital of a real country.",
    )
    async def cap(self, ctx, *, country):
        data = await country_filter(country, ctx)
        if data is None:
            return
        result = data["capital"]
        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        embed = discord.Embed(
            title=f"Capital of {country} — {alpha2} | {alpha3}",
            description="**The capital of {country} is `{result}`**".format(
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

    @commands.command(
        description="Check the population of a real country.",
        brief="Check the population of a real country.",
    )
    async def population(self, ctx, *, country):
        data = await country_filter(country, ctx)
        if data is None:
            return
        result = data["population"]
        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        embed = discord.Embed(
            title=f"Population of {country} — {alpha2} | {alpha3}",
            description="**The population of {country} is `{result:,}`**".format(
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

    @commands.command(
        description="Check the states/provinces in a real country",
        brief="Check the states/provinces in a real country",
    )
    async def states(self, ctx, *, country):
        data = await country_filter(country, ctx)
        if data is None:
            return

        country = data["name"]
        country1 = CountryInfo(country)

        result = country1.provinces()

        for i, x in enumerate(result):
            result[i] = "`" + x + "`"

        result1 = " |".join(result)

        result2 = re.sub(r"(?<=[|])(?=[^\s])", r" ", result1)

        embed = discord.Embed(
            title="States of " + country,
            description="**{result2}**".format(result2=result2),
            color=0xFF5733,
        )

        result4 = coco.convert(names=country, to="ISO2")
        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{result4.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)

    @commands.command(
        description="Check the main language of any real country.",
        brief="Check the main language of any real country.",
    )
    async def language(self, ctx, *, country):
        data = await country_filter(country, ctx)
        if data is None:
            return

        result1 = data["languages"]
        result = ""

        for i in result1:
            name = i["name"]
            result += f"`{name}` "

        country = data["name"]
        alpha2 = data["alpha2Code"]
        alpha3 = data["alpha3Code"]
        embed = discord.Embed(
            title=f"Languages of {country} — {alpha2} | {alpha3}",
            description="{result}".format(result=result),
            color=0xFF5733,
        )

        embed.set_thumbnail(url=f"https://flagcdn.com/w80/{alpha2.lower()}.jpg")

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.author),
            icon_url=ctx.author.avatar_url,
        )

        await ctx.send(embed=embed)

    @commands.command(
        description="Get COVID-19 data on a real country.",
        brief="Get COVID-19 data on a real country.",
    )
    async def covid(self, ctx, *, country):
        country = await country_filter(country, ctx)
        if country is None:
            return
        arg = country["name"]
        try:
            url = "https://covid-193.p.rapidapi.com/statistics?country={}".format(arg)

            headers = {
                "x-rapidapi-key": "f3c7547811mshb7e5680d6a29edcp1387fcjsncb14f156c54a",
                "x-rapidapi-host": "covid-193.p.rapidapi.com",
            }

            response = requests.request("GET", url, headers=headers)
            new_dict = json.loads(response.text)

            dict1 = new_dict["response"]

            dict2 = dict1[0]
            dict3 = dict2["cases"]
            new_cases = dict3["new"]
            active_cases = dict3["active"]
            critical_cases = dict3["critical"]
            recovered = dict3["recovered"]
            cases_per1mill = dict3["1M_pop"]
            total_cases = dict3["total"]

            deaths = dict2["deaths"]

            deaths_per1mill = deaths["1M_pop"]

            new_deaths = deaths["new"]

            total_deaths = deaths["total"]

            day = dict2["day"]

            if not new_cases:
                pass
            else:
                new_cases = new_cases[1:]
                new_cases = "{:,}".format(int(new_cases))
            if not active_cases:
                pass
            else:
                active_cases = "{:,}".format(int(active_cases))

            if not critical_cases:
                pass
            else:
                critical_cases = "{:,}".format(int(critical_cases))

            if not recovered:
                pass
            else:
                recovered = "{:,}".format(int(recovered))

            if not cases_per1mill:
                pass
            else:
                cases_per1mill = "{:,}".format(int(cases_per1mill))

            if not total_cases:
                pass
            else:
                total_cases = "{:,}".format(int(total_cases))

            if not deaths_per1mill:
                pass
            else:
                deaths_per1mill = "{:,}".format(int(deaths_per1mill))

            if not new_deaths:
                pass
            else:
                new_deaths = "{:,}".format(int(new_deaths))

            if not total_deaths:
                pass
            else:
                total_deaths = "{:,}".format(int(total_deaths))

            embed = discord.Embed(
                title="Covid 19 info for " + arg,
                description=None,
                color=Color.from_rgb(0, 0, 0),
            )

            embed.add_field(
                name="Cases",
                value=f"""New cases: `{new_cases}`
                                Active cases: `{active_cases}`
                                Critical cases: `{critical_cases}`
                                Recovered: `{recovered}`
                                Cases per 1 million people: `{cases_per1mill}`
                                Total cases: `{total_cases}`""",
                inline=True,
            )

            embed.add_field(
                name="Deaths",
                value=f"""New deaths: `{new_deaths}`
      Deaths per 1 million people: `{deaths_per1mill}`
      Total deaths: `{total_deaths}`""",
                inline=True,
            )

            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/239446877953720321/691020838379716698/unknown.png"
            )

            embed.set_footer(text=f"Date: {datetime.datetime.now()}")

            await ctx.channel.send(embed=embed)

        except:
            embed = discord.Embed(
                title="Sorry",
                description="**We could not find data for {}**".format(arg),
                color=0xFF5733,
            )

            embed.set_thumbnail(
                url="https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg"
            )

            await ctx.channel.send(embed=embed)

    @commands.command(
        description="View information about the bot",
        brief="View information about the bot",
    )
    async def stats(self, ctx):
        current_process = psutil.Process()
        cpu_usage = current_process.cpu_percent()
        memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000
        current_time = time.time()
        difference = int(round(current_time - main_up))
        text = str(datetime.timedelta(seconds=difference))

        embed = discord.Embed(title="Stats", color=Color.teal())

        embed.add_field(
            name="Server Count",
            value=f"""```css
[{len(self.bot.guilds)} servers]```""",
        )

        embed.add_field(
            name="CPU usage",
            value=f"""```css
[{cpu_usage}%]```""",
            inline=True,
        )

        embed.add_field(
            name="Uptime",
            value=f"""```css
[{text}]```""",
        )
        embed.add_field(
            name="Memory",
            value=f"""```ini
[{memory} kb]```""",
        )

        embed.add_field(
            name="User Countries",
            value=f"""```ini
[{await count()}]```""",
        )

        embed.add_field(
            name="Creator",
            value=f"""```ini
[Coder N#0001]```""",
            inline=True,
        )

        embed.add_field(
            name="Websocket Ping",
            value=f"""```ini
[{self.bot.latency * 1000} ms]```""",
        )

        embed.add_field(
            name="Commands",
            value=f"""```css
[{len(self.bot.commands)}]```""",
        )

        embed.set_footer(
            text="If some percentages show 0.0%, it means that the number is really close to zero."
        )
        await ctx.channel.send(embed=embed)

    @commands.command(
        brief="Get information from wikipedia! If searching up names please use full names; short names can cause ambiguity",
        description="Get information from wikipedia! If searching up names please use full names; short names can cause ambiguity",
        aliases=["wikipedia"],
    )
    async def wiki(self, ctx, *, page):
        try:
            data = wikipedia.page(page)

            await ctx.send(
                embed=discord.Embed(
                    title=data.title, url=data.url, description=data.summary
                )
            )
        except discord.errors.HTTPException:
            data = wikipedia.page(page)

            await ctx.send(
                embed=discord.Embed(
                    title=data.title,
                    url=data.url,
                    description=data.summary.split("\n")[0],
                )
            )
        except wikipedia.exceptions.DisambiguationError as e:
            await ctx.send(
                embed=discord.Embed(
                    title="Did you mean", description=", ".join(e.options)
                )
            )

        except wikipedia.exceptions.PageError:
            await ctx.send(":x: We could not find any matches for this page")


def setup(bot):
    bot.add_cog(General(bot))
