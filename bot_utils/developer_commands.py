from discord.ext import commands
import discord
import contextlib
import textwrap
import io
from bot_utils.background_tasks import BackgroundTasks
from bot_utils.mongomethods import findall


class DeveloperCommands(
    commands.Cog,
    name="Developer Commands",
    description="Commands that only the developer can use.",
):
    def __init__(self, bot, task):
        self.bot = bot
        self.task = task

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
            self.task.cancel()
            await ctx.channel.send("refugee drops have stopped")

    @commands.command(
        name="restart-presence",
        brief="A developer command to restart country bots status.",
        description="A developer command to restart country bots status.",
    )
    @commands.is_owner()
    async def restart_presence(self, ctx):
        await BackgroundTasks().presence()
        await ctx.send("Did it!")

    @commands.command(
        description="A developer only command to start refugee drops in the support server.",
        brief="A developer only command to start refugee drops in the support server.",
    )
    @commands.is_owner()
    async def start_drops(self, ctx):
        try:
            self.task = self.bot.loop.create_task(BackgroundTasks().refugee_drops())
            await ctx.channel.send("refugee drops have started")
        except:
            await ctx.channel.send("Drops are have already started")

    @commands.command(
        name="eval",
        aliases=["exec"],
        description="A developer only command, it can run code.",
        brief="A developer only command, it can run code.",
    )
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        code = code.strip("```py")
        code = code.strip("```Python")
        code = code.strip("```python")

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
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

    @commands.command(
        description="A developer only command to send an update about the bot to any servers who have set up an update channel.",
        brief="Sends an update about the bot to any servers who have set up an update channel.",
    )
    @commands.is_owner()
    async def send_update(self, ctx, *, info):
        embed = discord.Embed(title="Update!!!", description=info)
        for i in findall():
            await self.bot.get_channel(i["_id"]).send(embed=embed)
