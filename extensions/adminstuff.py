from discord.ext import commands
import discord
from mongomethods import update_prefix, get_prefix

@commands.command()
async def changeprefix(ctx, *, prefix):  
    if ctx.message.author.guild_permissions.administrator:
      if '<@810662403217948672>' in prefix or '<@!810662403217948672>' in prefix:
        await ctx.send('Invalid prefix')
      await update_prefix(ctx.guild.id, prefix)

      await ctx.channel.send(f"Prefix has been changed to `{prefix}`")
    else:
      await ctx.channel.send("You don't have sufficient permissions to do that")

@changeprefix.error
async def changeprefix_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    prefix = await get_prefix(ctx.guld.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}changeprefix <prefix>```')
    await ctx.channel.send(embed=embed)

  else:
    embed = discord.Embed(title='Error', description=f'''```-diff
    {error}''', color=0xe74c3c)

def setup(bot):
    bot.add_command(changeprefix)