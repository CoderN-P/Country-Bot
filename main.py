# imports form dicord.py
from discord.ext.commands import has_permissions
import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import cooldown

dic = {
    1: "Mom's basement",
    2: "Apartment (with roomate)",
    3: "Home Office",
    5: "Mansion",
    10: "Space Base",
}

# imports for eval command
from pathlib import Path
import textwrap
import contextlib
from traceback import format_exception

from pretty_help import DefaultMenu, PrettyHelp


# imports for mongodb

# imports for data on countries
from countryinfo import CountryInfo
import country_converter as coco
from emojiflags.lookup import lookup

# imports for json


# imports for checking text
from fuzzywuzzy import fuzz

import regex as re
import requests

# other
import random
import io
import os
import topgg
from dotenv import load_dotenv

load_dotenv()
# asyncio
import asyncio
from discord_slash import SlashCommand

# internal imports
from mongomethods import *


guild_ids = [821872779523522580]
# getting the prefix of the guild from replit db
def get_prefix123(bot, msg):
    if msg.guild.id is None:
        return "."
    try:
        prefix = get_prefix2(msg.guild.id)
    except:
        create_prefix2(msg.guild.id, ".")
        return "."
    return prefix


# creating bot instance


async def country_filter(country, ctx):
    if len(country) in [3, 2]:
        data = requests.get(f"https://restcountries.eu/rest/v2/alpha/{country}")
        data = data.json()

    else:
        data = requests.get(
            f"https://restcountries.eu/rest/v2/name/{country}?fullText=true"
        )
        data = data.json()
        if "status" in data:
            data = requests.get(f"https://restcountries.eu/rest/v2/name/{country}")
            data = data.json()
            if len(data) == 1:
                pass
            else:
                if "status" in data:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description=":x: Hm, I could not find a country with that name!",
                        )
                    )
                    return
                close_dict = {}

                for i, x in enumerate(data):
                    close_dict[i] = fuzz.ratio(country, x["name"])

                index = max(close_dict, key=close_dict.get) if close_dict else None

                if index:
                    data = data[index]
                else:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description=":x: Hm, I could not find a country with that name!",
                        )
                    )
                    return

    if "status" in data:
        await ctx.send(
            embed=discord.Embed(
                title="Error",
                description=":x: Hm, I could not find a country with that name!",
            )
        )

    else:
        if isinstance(data, list):
            data = data[0]
        return data


description = "Check out our slash commands! Type `/` to bring up all of the slash commands! If you do not see any slash commands from country bot, then please kick country bot and use [this link to invite it again](https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands)"
bot = commands.Bot(
    command_prefix=get_prefix123,
    case_insensitive=True,
    help_command=None,
    description=description,
)

slash = SlashCommand(bot, sync_commands=True)


menu = DefaultMenu("◀️", "▶️", "❌")  # You can copy-paste any icons you want.
ending_note = "Type {help.clean_prefix}help command to get information on a command\nType {help.clean_prefix}help category to get information on a category\nPlease do not put text in <> or []\n<> = mandatory argument, [] = optional argument"
bot.help_command = PrettyHelp(
    navigation=menu, color=discord.Colour.red(), ending_note=ending_note
)


bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "dbl_password")
bot.topgg_webhook.run(4355)

dbl_token = os.environ["TOPGGTOKEN"]
bot.topggpy = topgg.DBLClient(bot, dbl_token, autopost=True, post_shard_count=True)


@bot.event
async def on_autopost_success():
    print(
        f"Posted server count ({bot.topggpy.guild_count}), shard count ({bot.shard_count})"
    )


@bot.event
async def on_dbl_vote(data):
    """An event that is called whenever someone votes for the bot on Top.gg."""
    if data["type"] == "test":
        # this is roughly equivalent to
        # return await on_dbl_test(data) in this case
        return bot.dispatch("dbl_test", data)

    user = await bot.fetch_user(data["user"])
    try:
        a = await reading(user.id)
    except:
        await user.send(
            "Thanks for voting! Unfortunately since you have not made a country, you can't redeem any rewards :( To create a country type `.start` Remember, replace `.` with the prefix of the bot in the server you are in!"
        )
        return
    await update(
        (
            user.id,
            a[0][0],
            a[0][1] + (1000 * (a[0][5] + 1)),
            a[0][2],
            a[0][3],
            a[0][4],
            a[0][10],
        )
    )
    await update_coins((user.id, a[0][11] + (100 * a[0][5])))
    await user.send(
        "Thanks for voting, I apreciate it! Check your profile to see the received rewards!"
    )
    print(f"Received a vote:\n{data}")


@bot.event
async def on_dbl_test(data):
    """An event that is called whenever someone tests the webhook system for your bot on Top.gg."""
    user = await bot.fetch_user(data["user"])
    try:
        a = await reading(user.id)
    except:
        await user.send(
            "Thanks for voting! Unfortunately since you have not made a country, you can't redeem any rewards :( To create a country type `.start` Remember, replace `.` with the prefix of the bot in the server you are in!"
        )
        return
    await update(
        (
            user.id,
            a[0][0],
            a[0][1] + (1000 * (a[0][5] + 1)),
            a[0][2],
            a[0][3],
            a[0][4],
            a[0][10],
        )
    )
    await update_coins((user.id, a[0][11] + (100 * (a[0][5] + 1))))
    await user.send(
        "Thanks for voting, I apreciate it! Check your profile to see the received rewards!"
    )
    print(f"Received a test vote:\n{data}")


# add guild id to replit db when bot is added
@bot.event
async def on_guild_join(guild):
    await create_prefix(guild.id, ".")


# eremov guild id from replit db when bot is kicked
@bot.event
async def on_guild_remove(guild):
    await delete_prefix(guild.id)


# A command to change the prefix of the bot in that guild


def start_extensions(bot):
    bot.load_extension("extensions.adminstuff")
    bot.load_extension("extensions.misc")
    bot.load_extension("extensions.country_database")
    bot.load_extension("extensions.gambling")
    bot.load_extension("extensions.economy")
    bot.load_extension("extensions.memes")
    bot.load_extension("extensions.games")
    bot.load_extension("extensions.general")
    bot.load_extension("extensions.geographical")
    bot.load_extension("slash_commands.country_database")
    bot.load_extension("slash_commands.gambling")
    bot.load_extension("slash_commands.economy")
    bot.load_extension("slash_commands.memes")
    bot.load_extension("slash_commands.misc")
    bot.load_extension("slash_commands.games")
    bot.load_extension("slash_commands.adminstuff")
    bot.load_extension("slash_commands.general")
    bot.load_extension("slash_commands.geographical")
    bot.load_extension("jishaku")
    bot.add_cog(DeveloperCommands(bot))


async def presence():
    while True:
        await bot.change_presence(activity=discord.Game(name=".help"))
        await asyncio.sleep(10)
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="@Country Bot prefix"
            )
        )
        await asyncio.sleep(10)
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"{len(bot.guilds)} guilds"
            )
        )
        await asyncio.sleep(10)


# setting the status of the bot and sending a message if the guild is not in db


async def refugee_drops():

    words = ["come here!", "more people!", "🙂", "hello!"]

    channel = await bot.fetch_channel(836624980359643176)

    while True:
        word = random.choice(words)
        amount = random.randint(100, 1000)

        message = await channel.send(
            embed=discord.Embed(
                title="Refugees",
                description=f"{amount} refugees have showed up. Who will be the first person to bring them in! Say `{word}` to bring them in!!",
            )
        )

        def check(m):
            return m.content == word and m.channel == channel

        n = True
        while n:
            try:
                msg = await bot.wait_for("message", check=check, timeout=30)

                try:
                    a = await reading(msg.author.id)
                except:
                    embed = discord.Embed(
                        title="Sorry",
                        description=f":x: You don't have a country. Type `.start` to start one",
                    )
                    await msg.channel.send(embed=embed)
                    n = True

                await update(
                    (
                        msg.author.id,
                        a[0][0],
                        a[0][1] + amount,
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )
                await msg.reply(
                    embed=discord.Embed(
                        title="Hooray",
                        description=f"{amount} more people added to your country!",
                    )
                )

                break

            except asyncio.TimeoutError:
                await message.delete()
                break

        await asyncio.sleep(300)


@bot.event
async def on_ready():
    global task
    task = bot.loop.create_task(refugee_drops())
    bot.loop.create_task(presence())
    print("bot is ready")
    print(f"bot is in {len(bot.guilds)} servers")


# commands for the bot


# listening for the message that users send if they forgot their prefix


@bot.listen()
async def on_message(msg):

    if (
        msg.content == f"<@810662403217948672> prefix"
        or msg.content == f"<@!810662403217948672> prefix"
    ):
        prefix = bot.command_prefix(bot, msg)
        await msg.channel.send(f"My prefix in this server is `{prefix}`")

    elif (
        msg.content == f"<@810662403217948672>prefix"
        or msg.content == f"<@!810662403217948672>prefix"
    ):
        prefix = bot.command_prefix(bot, msg)
        await msg.channel.send(f"My prefix in this server is `{prefix}`")

    elif (
        msg.content == "<@810662403217948672>"
        or msg.content == "<@!810662403217948672>"
    ):
        prefix = bot.command_prefix(bot, msg)
        await msg.channel.send(f"My prefix in this server is `{prefix}`")


class DeveloperCommands(
    commands.Cog,
    name="Developer Commands",
    description="Commands that only the developer can use.",
):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="A developer only command to stop refugee drops in the support server.",
        brief="A developer only command to stop refugee drops in the support server.",
    )
    async def stop_drops(self, ctx):

        if int(ctx.author.id) != 751594192739893298:
            embed = discord.Embed(
                title="Hey!",
                description=":x: You don't have permission to use this command!",
            )
            await ctx.send(embed=embed)

        else:
            task.cancel()
            await ctx.channel.send("refugee drops have stopped")

    @commands.command(
        description="A developer only command to start refugee drops in the support server.",
        brief="A developer only command to start refugee drops in the support server.",
    )
    async def start_drops(self, ctx):
        if int(ctx.author.id) == 751594192739893298:
            try:
                global task
                task = bot.loop.create_task(refugee_drops())
                await ctx.channel.send("refugee drops have started")
            except:
                await ctx.channel.send("Drops are have already started")

    @commands.command(
        name="eval",
        aliases=["exec"],
        description="A developer only command, it can run code.",
        brief="A developer only command, it can run code.",
    )
    async def _eval(self, ctx, *, code):
        if ctx.author.id == 751594192739893298:
            code = code.strip("```py")
            code = code.strip("```Python")
            code = code.strip("```python")

            local_variables = {
                "discord": discord,
                "commands": commands,
                "bot": bot,
                "ctx": ctx,
                "channel": ctx.channel,
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message,
            }

            stdout = io.StringIO()

            try:
                with contextlib.redirect_stdout(stdout):
                    exec(
                        f"async def func():\n{textwrap.indent(code, '    ')}",
                        local_variables,
                    )

                    obj = await local_variables["func"]()
                    result = f"```py\n{stdout.getvalue()}\n-- {obj}\n```"
            except Exception as e:
                result = f"```py\n{e}```"

            await ctx.send(embed=discord.Embed(description=f"""{result}"""))

        else:
            embed = discord.Embed(
                title="Hey!",
                description=":x: You don't have permission to use this command!",
            )
            await ctx.send(embed=embed)

    @commands.command(
        description="A developer only command to send an update about the bot to any servers who have set up an update channel.",
        brief="Sends an update about the bot to any servers who have set up an update channel.",
    )
    @commands.is_owner()
    async def send_update(self, ctx, *, info):
        embed = discord.Embed(title="Update!!!", description=info)
        for i in findall():
            await bot.get_channel(i["_id"]).send(embed=embed)


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        main_message = ctx.message.content.split(" ")[0]

        similar = []
        other = []

        prefix = ctx.prefix

        for commands in bot.commands:

            if fuzz.ratio(main_message, commands.name) > 50:
                similar.append(f"`{prefix}{commands.name}`")
                other.append(commands)

        if len(similar) == 0:
            return
        similar = " ".join(similar)

        await ctx.channel.send(f"Did you mean {similar}")

    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        pass

    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        try:
            await ctx.author.send(
                ":thinking: Something went wrong... Double check that I have permission to talk there. Anyways, this bug will be sent to our team to fix, please stand by!"
            )
        except:
            pass
        guild = bot.get_guild(821872779523522580)
        channel = discord.utils.get(guild.channels, name="bug-logs")
        await channel.send(
            embed=discord.Embed(
                title="Error in executing a command",
                description=f"New error when executing command: {ctx.command.name}\n**Error**: {error}",
            )
        )

    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(
            embed=discord.Embed(
                title="Incorrect Usage",
                description=f"Correct Usage: ```{ctx.prefix}{ctx.command.name} {ctx.command.signature}```",
                color=discord.Colour.red(),
            )
        )

    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        embed = discord.Embed(title="Hmm", description=error.args[0])
        embed.set_footer(
            text=f"""If a person's name has spaces in it, put it in quotes! \nExample: {ctx.prefix}gift "Coder N" 100"""
        )
        await ctx.send(embed=embed)

    else:
        raise error


if not os.getenv("TOKEN"):
    print("HEYYYYY. DON'T TRY TO STEAL MY TOKEN OK")
else:
    if __name__ == "__main__":
        start_extensions(bot)
        bot.run(os.getenv("TOKEN"))
