import discord
import requests
from fuzzywuzzy import fuzz


async def country_filter(country, ctx):
    if len(country) in [3, 2]:
        data = requests.get(
            f"https://restcountries.eu/rest/v2/alpha/{country}")
        data = data.json()

    else:
        data = requests.get(
            f"https://restcountries.eu/rest/v2/name/{country}?fullText=true")
        data = data.json()
        if "status" in data:
            data = requests.get(
                f"https://restcountries.eu/rest/v2/name/{country}")
            data = data.json()
            if len(data) == 1:
                pass
            else:
                if "status" in data:
                    await ctx.send(embed=discord.Embed(
                        title="Error",
                        description=":x: Hm, I could not find a country with that name!",
                    ))
                    return
                close_dict = {}

                for i, x in enumerate(data):
                    close_dict[i] = fuzz.ratio(country, x["name"])

                index = max(close_dict,
                            key=close_dict.get) if close_dict else None

                if index:
                    data = data[index]
                else:
                    await ctx.send(embed=discord.Embed(
                        title="Error",
                        description=":x: Hm, I could not find a country with that name!",
                    ))
                    return

    if "status" in data:
        await ctx.send(embed=discord.Embed(
            title="Error",
            description=":x: Hm, I could not find a country with that name!",
        ))

    else:
        if isinstance(data, list):
            data = data[0]
        return data
