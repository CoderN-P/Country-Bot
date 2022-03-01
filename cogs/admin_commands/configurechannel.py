from discord.ext import commands
from bot_utils.mongomethods import create_update, delete_update
import discord


@commands.command(
    brief="Set up a channel to receive updates about the bot",
    description="Set up a channel to receive updates about the bot",
)
@commands.has_permissions(administrator=True)
async def configurechannel(self, ctx, channel: discord.TextChannel):

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
