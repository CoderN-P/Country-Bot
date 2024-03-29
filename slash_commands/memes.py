import discord
import requests
from discord.ext import commands
import os
from discord_slash import cog_ext

username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
import datetime


class Memes_Animals2(
    commands.Cog,
    name="Animals and Memes (slash)",
    description="Get pics of animals, and wholesome memes from reddit!",
):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Get memes from r/wholesomememes")
    async def meme(self, ctx):
        await ctx.defer(hidden=True)
        data = requests.get(
            "https://meme-api.herokuapp.com/gimme/wholesomememes"
        ).json()
        meme = data
        channel_nsfw = ctx.channel.is_nsfw()
        title = meme["title"]

        if meme["nsfw"] == "True":
            if channel_nsfw:
                embed = discord.Embed(title=f"{title} [NSFW]", url=meme["postLink"])
                embed.set_image(url=meme["url"])
                author = meme["author"]
                likes = meme["ups"]
                embed.set_footer(text=f"Author: {author} | 👍 {likes}")
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Hey!",
                    description=":x: This meme is NSFW!!! You can only see it in an NSFW channel.",
                )
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=meme["title"], url=meme["postLink"])
            embed.set_image(url=meme["url"])
            author = meme["author"]
            likes = meme["ups"]
            embed.set_footer(text=f"Author: {author} | 👍 {likes}")
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Look at cute cat pics from r/cats")
    async def cat(self, ctx):
        await ctx.defer(hidden=True)
        try:
            data = requests.get("https://meme-api.herokuapp.com/gimme/cats").json()
            meme = data

            title = meme["title"]

            embed = discord.Embed(title=f"{title}", url=meme["postLink"])
            embed.set_image(url=meme["url"])
            author = meme["author"]
            likes = meme["ups"]
            embed.set_footer(text=f"Author: {author} | 👍 {likes}")
            await ctx.send(embed=embed)
        except:
            await ctx.send(
                "Whoops! I could not load a cat image this time! Please try again!"
            )

    @cog_ext.cog_slash(description="Look at cute dog pics from r/dogs")
    async def dog(self, ctx):
        await ctx.defer(hidden=True)
        try:
            data = requests.get("https://meme-api.herokuapp.com/gimme/dog").json()
            meme = data

            title = meme["title"]

            embed = discord.Embed(title=f"{title}", url=meme["postLink"])
            embed.set_image(url=meme["url"])
            author = meme["author"]
            likes = meme["ups"]
            embed.set_footer(text=f"Author: {author} | 👍 {likes}")
            await ctx.send(embed=embed)

        except:
            await ctx.send(
                "Whoops! I could not load a dog image this time! Please try again!"
            )

    @cog_ext.cog_slash(
        description="Look at pictures that make you go awwww. From r/aww"
    )
    async def aww(self, ctx):
        await ctx.defer(hidden=True)
        data = requests.get("https://meme-api.herokuapp.com/gimme/awww").json()
        meme = data

        title = meme["title"]

        embed = discord.Embed(title=f"{title}", url=meme["postLink"])
        embed.set_image(url=meme["url"])
        author = meme["author"]
        likes = meme["ups"]
        embed.set_footer(text=f"Author: {author} | 👍 {likes}")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Look at snakes")
    async def snake(self, ctx):
        await ctx.defer(hidden=True)
        data = requests.get("https://meme-api.herokuapp.com/gimme/snakes").json()
        meme = data

        title = meme["title"]

        embed = discord.Embed(title=f"{title}", url=meme["postLink"])
        embed.set_image(url=meme["url"])
        author = meme["author"]
        likes = meme["ups"]
        embed.set_footer(text=f"Author: {author} | 👍 {likes}")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description="Create a drake meme. The meme_format should be: meme title | meme text 1 | meme text 2"
    )
    async def drake(self, ctx, *, meme_format: str):
        await ctx.defer(hidden=True)
        arg = meme_format
        data = requests.get("https://api.imgflip.com/get_memes").json()["data"]["memes"]
        images = [
            {"name": image["name"], "url": image["url"], "id": image["id"]}
            for image in data
        ]

        arg = arg.split("|")
        if len(arg) < 3:
            await ctx.send(
                embed=discord.Embed(
                    title="Incorrect Usage",
                    description=f"Correct Usage:\n```/drake meme title | meme text 1 | meme text 2```",
                )
            )
            return
        URL = "https://api.imgflip.com/caption_image"
        params = {
            "username": username,
            "password": password,
            "template_id": images[0]["id"],
            "text0": arg[1],
            "text1": arg[2],
        }
        response = requests.request("POST", URL, params=params).json()

        url = response["data"]["url"]

        embed = discord.Embed(title=arg[0])
        embed.set_image(url=url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Memes_Animals2(bot))
