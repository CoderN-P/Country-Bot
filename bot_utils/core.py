import os

import discord
import topgg
from discord.ext import commands
from discord_slash import SlashCommand
from fuzzywuzzy import fuzz
from pretty_help import DefaultMenu, PrettyHelp

from bot_utils.background_tasks import BackgroundTasks
from bot_utils.mongomethods import (
    create_prefix,
    create_prefix2,
    delete_prefix,
    get_prefix2,
    reading,
    update,
    update_coins,
)


class CountryBot(commands.Bot):

    def __init__(self):
        self.owner = 751594192739893298
        self.description = "Check out our slash commands! Type `/` to bring up all of the slash commands! If you do not see any slash commands from country bot, then please kick country bot and use [this link to invite it again](https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands)"
        super().__init__(
            command_prefix=self.get_prefix123,
            help_command=None,
            description=self.description,
            case_insensitive=True,
            owner_id=self.owner,
        )
        _ = SlashCommand(self, sync_commands=True)

        self.topgg_webhook = topgg.WebhookManager(self).dbl_webhook(
            "/dblwebhook", "dbl_password")
        self.topgg_webhook.run(4355)

        menu = DefaultMenu("◀️", "▶️",
                           "❌")  # You can copy-paste any icons you want.
        ending_note = "Type {help.clean_prefix}help command to get information on a command\nType {help.clean_prefix}help category to get information on a category\nPlease do not put text in <> or []\n<> = mandatory argument, [] = optional argument"
        self.help_command = PrettyHelp(navigation=menu,
                                       color=discord.Colour.red(),
                                       ending_note=ending_note)
        dbl_token = os.environ["TOPGGTOKEN"]
        self.topggpy = topgg.DBLClient(self,
                                       dbl_token,
                                       autopost=True,
                                       post_shard_count=True)

        self.tasks = BackgroundTasks(self)

    def get_prefix123(bot, msg):
        if msg.guild.id is None:
            return "."
        try:
            prefix = get_prefix2(msg.guild.id)
        except:
            create_prefix2(msg.guild.id, ".")
            return "."
        return prefix

    def run(self):
        self.run(os.getenv("TOKEN"))

    async def on_message(self, msg):
        if (msg.content == f"<@810662403217948672> prefix"
                or msg.content == f"<@!810662403217948672> prefix"):
            prefix = self.bot.command_prefix(self.bot, msg)
            await msg.channel.send(f"My prefix in this server is `{prefix}`")

        elif (msg.content == f"<@810662403217948672>prefix"
              or msg.content == f"<@!810662403217948672>prefix"):
            prefix = self.bot.command_prefix(self.bot, msg)
            await msg.channel.send(f"My prefix in this server is `{prefix}`")

        elif (msg.content == "<@810662403217948672>"
              or msg.content == "<@!810662403217948672>"):
            prefix = self.bot.command_prefix(self.bot, msg)
            await msg.channel.send(f"My prefix in this server is `{prefix}`")

    async def on_ready(self):
        self.drops = self.bot.loop.create_task(self.tasks.refugee_drops())
        self.bot.loop.create_task(self.tasks.presence())
        print("bot is ready")
        print(f"bot is in {len(self.bot.guilds)} servers")

    async def on_autopost_success(self):
        print(
            f"Posted server count ({self.topggpy.guild_count}), shard count ({self.shard_count})"
        )

    async def on_dbl_vote(self, data):
        if data["type"] == "test":
            # this is roughly equivalent to
            # return await on_dbl_test(data) in this case
            return self.dispatch("dbl_test", data)

        user = await self.fetch_user(data["user"])
        try:
            a = await reading(user.id)
        except:
            await user.send(
                "Thanks for voting! Unfortunately since you have not made a country, you can't redeem any rewards :( To create a country type `.start` Remember, replace `.` with the prefix of the bot in the server you are in!"
            )
            return
        await update((
            user.id,
            a[0][0],
            a[0][1] + (1000 * (a[0][5] + 1)),
            a[0][2],
            a[0][3],
            a[0][4],
            a[0][10],
        ))
        await update_coins((user.id, a[0][11] + (100 * a[0][5])))
        await user.send(
            "Thanks for voting, I appreciate it! Check your profile to see the received rewards!"
        )
        print(f"Received a vote:\n{data}")

    async def on_guild_join(self, guild):
        await create_prefix(guild.id, ".")

    async def on_guild_remove(self, guild):
        await delete_prefix(guild.id)

    async def on_command_error(self, ctx, error):

        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            main_message = ctx.message.content.split(" ")[0]

            similar = []
            other = []

            prefix = ctx.prefix

            for commands in self.bot.commands:

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
            guild = self.bot.get_guild(821872779523522580)
            channel = discord.utils.get(guild.channels, name="bug-logs")
            await channel.send(embed=discord.Embed(
                title="Error in executing a command",
                description=f"New error when executing command: {ctx.command.name}\n**Error**: {error}",
            ))

        elif isinstance(error,
                        discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title="Incorrect Usage",
                description=f"Correct Usage: ```{ctx.prefix}{ctx.command.name} {ctx.command.signature}```",
                color=discord.Colour.red(),
            ))

        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            embed = discord.Embed(title="Hmm", description=error.args[0])
            embed.set_footer(
                text=f"""If a person's name has spaces in it, put it in quotes! \nExample: {ctx.prefix}gift "Coder N" 100"""
            )
            await ctx.send(embed=embed)

        if isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command!")

        else:
            raise error

    def load_cogs(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.bot.load_extension(f"cogs.{filename[:-3]}")
