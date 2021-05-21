from mongomethods import count, reading, update, update_prestige, update_war, writing, delete_task, search_name, update_coins, find_inventory, create_update, findall, delete_update, update_inventory

from fuzzywuzzy import fuzzywuzzy

from emojiflags.lookup import lookup

import unicodedata

from main import quiz_country_list


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






class WarCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  
  @commands.command()
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def war(self, ctx, user):
    b = user
    b = b.replace("<","")
    b = b.replace(">","")
    b = b.replace("@","")
    b = b.replace("!", "")

    
    try:

      if int(b) == int(ctx.message.author.id):
        embed = discord.Embed(title='Stop!', description=":x: You can't wage war on yourself!")
        await ctx.channel.send(embed=embed)
        return
    except:
      embed= discord.Embed(title='Sorry', description=f''':x: This user doesn't have a country yet''')

      await ctx.channel.send(embed=embed)
      return
    try:
      user1 = reading(ctx.message.author.id)
    except:
      embed= discord.Embed(title='Sorry', description=f''':x: You don't have a country yet. Type {db[str(ctx.guild.id)]}start to create your amazing country!!!''')

      await ctx.channel.send(embed=embed)
      return
    try:
      user2 = reading(b)
    except:
      embed= discord.Embed(title='Sorry', description=f''':x: This user doesn't have a country yet''')

      await ctx.channel.send(embed=embed)
      return
    
    await ctx.channel.send(f"{user}, you have 20 seconds to accept <@!{ctx.message.author.id}> request to war. Type `accept` in the chat to accept, or type `deny` in the chat to end the conflict")

    opponent = await bot.fetch_user(b)
    def check(m):
      return m.channel == ctx.channel and m.author == opponent and m.content.lower() == 'accept' or m.content.lower() == 'deny'
    try:
      msg = await self.bot.wait_for('message', check=check, timeout=20)
    except asyncio.TimeoutError:
      embed = discord.Embed(title='Whoops', description=':x: Time ran out. The war preperations took too long. No war')
      await ctx.channel.send(embed=embed)
      return


    if msg.content.lower() == 'accept':
      embed = discord.Embed(title='Accepted', description=f"<@!{ctx.message.author.id}> your opponent accepted!!")
      await ctx.channel.send(embed=embed)
    else:
      embed=discord.Embed(title='Phew', dsescription='Crisis averted. There is no war')
      await ctx.channel.send(embed=embed)
      return

    
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.message.author
    n = True  
    while n:
      await ctx.channel.send(f"<@!{ctx.message.author.id}> how many troops do you want to deploy, type `quit` to end")
      try:
        msg = await self.bot.wait_for('message', check=check, timeout=20)
      except asyncio.TimeoutError:
          await ctx.channel.send("Time ran out. No war :(")
          return

    
      
      try:
        num = float(msg.content)
        
        if num == 0:
          await ctx.channel.send("You can't go to war with 0 people smh")
          continue
          
        else:
          pass

        
      except:
        if msg.content.lower().startswith('quit'):
          await ctx.send(':x: Game quit')
          return
        await ctx.channel.send("That is not a valid amount!!")
        continue

      if num.is_integer():
        if int(msg.content) < user1[0][1]:
          await ctx.channel.send(f"{msg.content} people deployed")
          user1_troops = int(msg.content)
          break
        else:
          await ctx.channel.send(f":x: <@!{ctx.message.author.id}> you dont have enough people!!!!")
          continue
      else:
        await ctx.channel.send(f"{msg.content} is not a valid amount")
        continue


    def check(m):
      return m.channel == ctx.channel and m.author == opponent

    while n:
      await ctx.channel.send(f"{user} how many troops do you want to deploy, type `quit` to end")
      try:
        msg = await self.bot.wait_for('message', check=check, timeout=20)
      except asyncio.TimeoutError:
          await ctx.channel.send("Time ran out. No war :(")
          return
      try:
        num = float(msg.content)

        if num == 0:
          await ctx.channel.send("You can't go to war with 0 people smh")
          continue
      except:
        await ctx.channel.send("That is not a valid amount!!")
        continue

      if num.is_integer():
        if int(msg.content) < user2[0][1]:
          await ctx.channel.send(f"{msg.content} people deployed")
          user2_troops = int(msg.content)
          break
        else:
          await ctx.channel.send(f":x: {user} you dont have enough people!!!!")
          continue
      else:
        await ctx.channel.send(f"{msg.content} is not a valid amount")
        continue

    random_country = random.choice(quiz_country_list)
    country_capital1 = CountryInfo(random_country)
    country_capital = country_capital1.capital()

    if not country_capital:
      random_country = random.choice(quiz_country_list)
      country_capital1 = CountryInfo(random_country)
      country_capital = country_capital1.capital()


    country_capital = unicodedata.normalize('NFKD', country_capital).encode('ascii', 'ignore').decode('utf-8')
    


    #try:

    result4 = coco.convert(names=random_country, to='ISO2')

    await ctx.channel.send(f"What is the capital of....... `{random_country.title()}` {lookup(result4)}")

    #except:
      #await ctx.channel.send(f"What is the capital of....... `{random_country}`")

    
    def check(m):
      
      return m.content.lower() == country_capital.lower() and m.channel == ctx.channel and int(m.author.id) in [int(b), int(ctx.message.author.id)]

    try:
      msg = await self.bot.wait_for('message', check=check, timeout=30)
      
      
    except asyncio.TimeoutError:
      await ctx.channel.send('Time ran out. Draw!!!')
      return

    if msg.author == ctx.author:
        await ctx.channel.send(f'<@!{ctx.message.author.id}> you gave the answer first. You won the war!!! :crown:')
        update_war((ctx.message.author.id, user1[0][0], user1[0][1] + user2_troops, user1[0][2], user1[0][3], user1[0][4], user1[0][5], user1[0][6], user1[0][7] + 1, user1[0][8] + 1, user1[0][9]))

        update_war((b, user2[0][0], user2[0][1] - user2_troops, user2[0][2], user2[0][3], user2[0][4], user2[0][5], user2[0][6], user2[0][7] + 1, user2[0][8], user2[0][9] + 1))
      
    else:
        await ctx.channel.send(f'{user} you gave the answer first. You won the war!!! :crown:')
        update_war((ctx.message.author.id, user1[0][0], user1[0][1] - user1_troops, user1[0][2], user1[0][3], user1[0][4], user1[0][5], user1[0][6], user1[0][7] + 1, user1[0][8], user1[0][9] + 1))

        update_war((b, user2[0][0], user2[0][1] + user1_troops, user2[0][2], user2[0][3], user2[0][4], user2[0][5], user2[0][6], user2[0][7] + 1, user2[0][8] + 1, user2[0][9]))



    @war.error
    async def war_error(self, ctx, error):
      if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}war <user>``` User should be a ping')
        await ctx.channel.send(embed=embed)

      elif isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title="Hey!",description=f'''You can't wage war right now! Try again in `{error.retry_after:.2f}`s.''')
            await ctx.send(embed=em)


def setup(bot):
  bot.add_command(tax)
  bot.add_cog(WarCog(bot))