from mongomethods import count, reading, update, update_prestige, update_war, writing, delete_task, search_name, update_coins, find_inventory, create_update, findall, delete_update, update_inventory


from replit import db



import discord
from discord.ext import commands







@commands.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def tax(ctx):
  try:
    a = reading(ctx.author.id)

  except:
    embed = discord.Embed(title='Hey!', description=f":x: You don't have a country! Type {db[str(ctx.guild.id)]} to start one!")

    await ctx.send(embed=embed)
    return

  if a[0][11] > 1000000000:
    embed = discord.Embed(title='Hey!', description="You can't tax more. You have emptied the money supply!")
    await ctx.send(embed=embed)
    return

  
  tax1 = round((round((a[0][1] ** 0.5)/ 100)  * a[0][5] + 1))

  await ctx.send(embed=discord.Embed(title='Tax', description=f'You got {tax1} :coin: from taxing your population'))

  update_coins((ctx.author.id, tax1 + a[0][11]))

@tax.error
async def tax_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="Hey!",description=f'''You can't collect taxes now! Try again in `{error.retry_after:.2f}`s.''')
        await ctx.send(embed=em)






 


def setup(bot):
  bot.add_command(tax)