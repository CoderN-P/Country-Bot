from discord.ext import commands
import discord
from bot_utils.mongomethods import delete_update


@commands.command(
    brief="Make a channel not receive updates about the bot",
    description="Make a channel not receive updates about the bot",
)
@commands.has_permissions(administrator=True)
async def unconfigurechannel(self, ctx, channel: discord.TextChannel):
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
            title="Success", description=f" {channel} won't receive update messages"
        )
    )
