from discord.ext import commands
import discord
import requests
import os
import datetime
import time
import random
import json
from discord_slash import cog_ext


class Misc2(commands.Cog, description="Miscellaneous commands (slash)"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="cat-fact", description="Learn some cool cat facts!")
    async def catfact(self, ctx):
        await ctx.defer(hidden=True)
        r = requests.get("https://catfact.ninja/fact?max_length=140")
        r = r.json()["fact"]
        embed = discord.Embed(title="Cat Fact", description=r)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="dog-fact", description="Learn some cool dog facts!")
    async def dogfact(self, ctx):
        await ctx.defer(hidden=True)
        r = requests.get("http://dog-api.kinduff.com/api/facts?number=1")
        r = r.json()["facts"][0]
        embed = discord.Embed(title="Dog Fact", description=r)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Get Country Bot's invite link")
    async def invite(self, ctx):
        await ctx.defer(hidden=True)
        await ctx.send(
            embed=discord.Embed(
                title="Invite link",
                description="Use this link to invite the bot to your servers: https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands",
            )
        )

    @cog_ext.cog_slash(description="bruh")
    async def bruh(self, ctx):
        await ctx.defer(hidden=True)
        embed = discord.Embed(title="bruh")
        embed.set_image(
            url="https://media1.tenor.com/images/8daeb547b121eef5f34e7d4e0b88ea35/tenor.gif?itemid=5156041"
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description="Get a random joke, or specify a type of joke: `knock-knock`, `general`, or `programming`"
    )
    async def joke(self, ctx, *, type: str = None):
        await ctx.defer(hidden=True)
        arg = type

        def jokes(f):
            data = requests.get(f)
            tt = json.loads(data.text)
            return tt

        error_embed = discord.Embed(
            title="Error",
            description=":x: That is not a valid option! The valid options are, `knock-knock` `general` and `programming`",
        )
        if arg:
            if " ".join(arg) == "knock knock":
                f = f"https://official-joke-api.appspot.com/jokes/knock-knock/random"
                a = jokes(f)

                for i in a:
                    await ctx.send(
                        embed=discord.Embed(
                            title=i["setup"], description=i["punchline"]
                        )
                    )
                return
            if arg not in ["knock-knock", "general", "programming"]:
                await ctx.send(embed=error_embed)
                return
            f = f"https://official-joke-api.appspot.com/jokes/{arg}/random"
            a = jokes(f)

            for i in a:
                await ctx.send(
                    embed=discord.Embed(title=i["setup"], description=i["punchline"])
                )

        else:
            joke = random.choice(["knock-knock", "general", "programming"])

            f = f"https://official-joke-api.appspot.com/jokes/{joke}/random"
            a = jokes(f)

            for i in a:
                embed = discord.Embed(title=i["setup"], description=i["punchline"])
                embed.set_footer(text=f"This was a {joke} joke")
                await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Vote for Country Bot to get some cool rewards!")
    async def vote(self, ctx):
        await ctx.defer(hidden=True)
        embed = (
            discord.Embed(
                title="Vote For Country Bot :)",
                description="You can vote for country bot [here](https://top.gg/bot/810662403217948672/vote)",
            )
            .set_image(url="https://top.gg/images/dblnew.png")
            .set_footer(text="You can vote every 12 hours")
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Get the message ping of the bot.")
    async def ping(self, ctx):
        await ctx.defer(hidden=True)
        """Pong!"""
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")

    @cog_ext.cog_slash(description="N o t h i n g")
    async def nothing(self, ctx):
        await ctx.defer(hidden=True)
        await ctx.send("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")

    @cog_ext.cog_slash(
        description="Get information about a color by supplying its rgb/hex"
    )
    async def color(self, ctx, *, color: str):
        await ctx.defer(hidden=True)
        rgb = color
        if rgb.startswith("#"):
            info = requests.get(f"https://www.thecolorapi.com/id?hex={rgb[1:]}")
        else:
            info = requests.get(f"https://www.thecolorapi.com/id?rgb={rgb}")

        try:
            info = info.json()

            hex1 = info["hex"]["value"]

            rgb1 = info["rgb"]["value"][:-1]

            rgb1 = rgb1[4:]

            readableHex = int(hex(int(hex1.replace("#", ""), 16)), 0)

            name = info["name"]["value"]

            cmyk = info["cmyk"]["value"][5:][:-1]
            cmyk.replace("NaN", "0")

            hsl = info["hsl"]["value"][4:][:-1]

            hsl.replace("%", "")

            hsv = info["hsv"]["value"][4:][:-1]
            hsv.replace("%", "")

            xyz = info["XYZ"]["value"][4:][:-1]

            rgb2 = rgb1.split(",")
            rgb2 = [float(i) for i in rgb2]

            embed = discord.Embed(title=name, description=None, color=readableHex)

            embed.add_field(name="RGB", value=rgb1, inline=True)
            embed.add_field(name="HEX", value=hex1)

            embed.add_field(name="CMYK", value=cmyk)
            embed.add_field(name="HSL", value=hsl)
            embed.add_field(name="HSV", value=hsv, inline=True)
            embed.add_field(name="XYZ", value=xyz, inline=True)

            embed.set_image(
                url=f"https://singlecolorimage.com/get/{hex1[1:]}/400x100.png"
            )
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(
                title="Error",
                description=":x: Invalid Hex or RGB\n Example usage: ```/color 100, 200, 150``` or ```/color #some hex```",
            )
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="lol")
    async def lol(self, ctx):
        await ctx.defer(hidden=True)
        embed = discord.Embed(title="LOL")

        embed.set_image(
            url="https://freepngimg.com/thumb/internet_meme/11-2-lol-face-meme-png.png"
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Country Bot changelog.")
    async def changelog(self, ctx):
        await ctx.defer(hidden=True)
        embed = discord.Embed(
            title="Changelog",
            description="""**1.** Added new `.meme` feature
    **2.** New `.coinflip` feature
    **3.** Added statistics for `work commands issued`
    **4.** Added Statistics for `war` on country profiles
    **5.** Added a special feature only in the support server
    **6.** Added new feature `.gift` (allows you to gift population to other users
    **7.** New autocorrect when you misspell a command
    """,
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="calc",
        description="Calculate a mathematical expression, (no variables allowed)",
    )
    async def my_command(self, ctx, *, expression: str):
        await ctx.defer(hidden=True)
        result = eval(expression)
        await ctx.send(result)

    @cog_ext.cog_slash(description="Country Bot will reverse the text you give it.")
    async def backwards(self, ctx, *, text: str):
        await ctx.defer(hidden=True)
        await ctx.send(text[::-1].strip("@"))

    @cog_ext.cog_slash(name="gummy-bear", description="Im a gummy bear.")
    async def gummy_bear(self, ctx):
        await ctx.defer(hidden=True)
        await ctx.send(
            "https://tenor.com/view/cbd-gummies-unlimited-gummy-bear-gif-12397676"
        )


def setup(bot):
    bot.add_cog(Misc2(bot))
