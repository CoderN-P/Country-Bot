from discord.ext import commands
import discord
from mongomethods import update_prefix, get_prefix, create_update, delete_update
import datetime
class AdminCommands(commands.Cog, name='Admin/Configuration', description='Commands only for admins'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(brief='Change the prefix of the bot on your server', description='Change the prefix of the bot on your server')
  async def changeprefix(self, ctx, *, prefix):  
      if ctx.message.author.guild_permissions.administrator:
        if '<@810662403217948672>' in prefix or '<@!810662403217948672>' in prefix:
          await ctx.send('Invalid prefix')
          return
        await update_prefix(ctx.guild.id, prefix)

        await ctx.channel.send(f"Prefix has been changed to `{prefix}`")
      else:
        await ctx.channel.send("You don't have sufficient permissions to do that")
  
  @commands.command(brief='Set up a channel to receive updates about the bot', description='Set up a channel to receive updates about the bot')
  @commands.has_permissions(administrator=True)
  async def configurechannel(self, ctx, channel: discord.TextChannel):
    
    try:
      await channel.send(embed=discord.Embed(title='Success', description='Channel is configured to receive updates about the bot!'))

    except:
      await ctx.send(embed=discord.Embed(title='Oh No!', description=":x: I couldn't send mesages in that channel. Please provide a valid channel!"))
      return

    try:
      await create_update(channel)
    except:
      await ctx.send(embed=discord.Embed(title='Hey!', description='This channel has already been configured!'))


  @configurechannel.error
  async def configure_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send("You need the `ADMINISTRATOR` permission to do that!")


  @commands.command(brief='Make a channel not receive updates about the bot', description='Make a channel not receive updates about the bot')
  @commands.has_permissions(administrator=True)
  async def unconfigurechannel(self, ctx, channel: discord.TextChannel):
    try:
      await delete_update(int(channel.id))

    except:
      await ctx.send(embed=discord.Embed(title='Oh No!', description=":x: Please provide a valid channel!"))
      return

    await ctx.send(embed=discord.Embed(title='Success', description=f" {channel} won't receive update messages"))

  @unconfigurechannel.error
  async def unconfigure_error(self, ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send("You need the `ADMINISTRATOR` permission to do that!")

def setup(bot):
    bot.add_cog(AdminCommands(bot))