from discord.ext import commands
from bot_utils.mongomethods import update_prefix


@commands.command(
    brief="Change the prefix of the bot on your server",
    description="Change the prefix of the bot on your server",
)
@commands.has_permissions(administrator=True)
async def changeprefix(self, ctx, *, prefix):
    if "<@810662403217948672>" in prefix or "<@!810662403217948672>" in prefix:
        await ctx.send("Invalid prefix")
        return
    await update_prefix(ctx.guild.id, prefix)

    await ctx.channel.send(f"Prefix has been changed to `{prefix}`")
