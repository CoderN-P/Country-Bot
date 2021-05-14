from discord.ext import commands
from mongomethods import count, reading, update, update_prestige, update_war, writing, delete_task, search_name, update_coins
from replit import db
import discord, random

@commands.command()
async def coinflip(ctx, *amount1):
  h_t = random.choice(['h', 't'])
  try:
    a = reading(ctx.author.id)
  except:
    embed = discord.Embed(title='Hey!', description=f":x: You don't have a country. Start a country with `{db[str(ctx.guild.id)]}start`")
    await ctx.channel.send(embed=embed)
    return

  amount = []
  for i in amount1:
    amount.append(i)


  try:
    
    if amount[0].lower() not in ['heads', 'tails']:
      embed = discord.Embed(title='huh', description=':x: That is not a valid option. Specify either `heads` or `tails`')
      await ctx.channel.send(embed=embed)
      return

    else:
      pass

  except:
    embed = discord.Embed(title='Error', description=':x: You need to specify heads or tails!')
    await ctx.channel.send(embed=embed)
    return

  
  if len(amount) == 1:
    if a[0][1] <= 0:
      embed = discord.Embed(title='Hey!', description=":x: You don't have enough people to do this command")
      await ctx.channel.send(embed=embed)
      return
    
    if h_t == 'h':
      confirmed = 'heads'

    else:
      confirmed = 'tails'

    if confirmed == amount[0]:
      embed = discord.Embed(title='Woohooooo!!!', description=':tada: Your guess was correct!! You won `1` population!!!')

      update((ctx.author.id, a[0][0], a[0][1] + 1, a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return

    else:
      embed = discord.Embed(title=':(', description=':slight_frown: Your guess was incorrect. You lost `1` population')

      update((ctx.author.id, a[0][0], a[0][1] - 1, a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return

  else:
    
    try:
      amount[1] = int(amount[1])
    except:
      embed = discord.Embed(title='Error', description=':x: You have entered an invalid amount!')
      await ctx.send(embed=embed)
      return


    if a[0][1] <= int(amount[1]):
      embed = discord.Embed(title='Hey!', description=":x: You don't have that much population to bet")
      await ctx.send(embed=embed)
      return
    
    if h_t == 'h':
      confirmed = 'heads'

    else:
      confirmed = 'tails'

    if confirmed == amount[0]:
      embed = discord.Embed(title='Woohooooo!!!', description=f':tada: Your guess was correct!! You won `{amount[1]}` population!!!')

      update((ctx.author.id, a[0][0], a[0][1] + int(amount[1]), a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return

    else:
      embed = discord.Embed(title=':(', description=f':slight_frown: Your guess was incorrect. You lost `{amount[1]}` population')

      update((ctx.author.id, a[0][0], a[0][1] - amount[1], a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return


def setup(bot):
  bot.add_command(coinflip)