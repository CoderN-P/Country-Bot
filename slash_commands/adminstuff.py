from discord.ext import commands
import discord
from mongomethods import update_prefix, create_update, delete_update
import datetime
from discord_slash import cog_ext


class AdminCommands2(
    commands.Cog,
    name="Admin/Configuration (slash)",
    description="Commands only for admins",
):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Set up a channel to receive updates about the bot")
    @commands.has_permissions(administrator=True)
    async def configurechannel(self, ctx, channel: discord.TextChannel):
        await ctx.defer(hidden=True)

        try:
            await create_update(channel.id)
        except:
            await ctx.send(
                embed=discord.Embed(
                    title="Hey!",
                    description="This channel has already been configured!",
                )
            )
            return

        try:
            await channel.send(
                embed=discord.Embed(
                    title="Success",
                    description="Channel is configured to receive updates about the bot!",
                )
            )
            await ctx.send(f"Great! {channel} is now configured!")
        except:
            await ctx.send(
                embed=discord.Embed(
                    title="Oh No!",
                    description=":x: I couldn't send mesages in that channel. Please provide a valid channel! Or make sure that I have permission to talk there!",
                )
            )
            await delete_update(channel.id)
            return

    @cog_ext.cog_slash(description="Make a channel not receive updates about the bot")
    @commands.has_permissions(administrator=True)
    async def unconfigurechannel(self, ctx, channel: discord.TextChannel):
        await ctx.defer(hidden=True)
        try:
            await delete_update(int(channel.id))

        except:
            await ctx.send(
                embed=discord.Embed(
                    title="Oh No!", description=":x: Please provide a valid channel!"
                )
            )
            return

        await ctx.send(
            embed=discord.Embed(
                title="Success", description=f"{channel} won't receive update messages"
            )
        )


def setup(bot):
    bot.add_cog(AdminCommands2(bot))
