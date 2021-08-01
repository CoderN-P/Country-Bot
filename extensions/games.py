from mongomethods import *

from fuzzywuzzy import fuzz
import country_converter as coco

from emojiflags.lookup import lookup

import datetime
import unicodedata, asyncio

from countryinfo import CountryInfo


from discord import Color
import random


import discord
from discord.ext import commands

dic2 = {'Mayor': 1, 'State Senator': 2, 'Governor': 3, 'Senator': 4, 'Vice President': 5, 'President': 6}

global dic
dic = {1 : "Mom's basement", 2 : 'Apartment (with roomate)', 3 : 'Home Office', 5 : 'Mansion', 10 : 'Space Base'}

hunt_animals = {'Boar': [':boar:', 1000], 'Deer': [':deer:', 400], 'Crocodile': [':crocodile:', 750]}

global quiz_country_list
quiz_country_list = list(CountryInfo().all().keys())


class EconomyCommands(commands.Cog, name='Economy Commands', description='Commands that let you have your own little economy system'):
  def __init__(self, bot):
    self.bot = bot
    

  @commands.command(brief='Tax your citizens for coins.', description='Tax your citiens for coins.')
  @commands.cooldown(1, 300, commands.BucketType.user)
  async def tax(self, ctx):
    try:
      a = await reading(ctx.author.id)

    except:
      prefix = await get_prefix(id)
      embed = discord.Embed(title='Hey!', description=f":x: You don't have a country! Type `{prefix}start` to start one!")

      await ctx.send(embed=embed)
      return

    if a[0][11] > 1000000000:
      embed = discord.Embed(title='Hey!', description="You can't tax more. You have emptied the money supply!")
      await ctx.send(embed=embed)
      return

    prestige = a[0][5] + 1

    
    tax1 = round(((a[0][1] ** 0.5)/50) * prestige)

    tax1 *= dic2[a[0][3]] 

    await ctx.send(embed=discord.Embed(title='Tax', description=f'You got {tax1} :coin: from taxing your population'))

    await update_coins((ctx.author.id, tax1 + a[0][11]))

  @tax.error
  async def tax_error(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
          em = discord.Embed(title="Hey!",description=f'''You can't collect taxes now! Try again in `{error.retry_after:.2f}`s.''')
          await ctx.send(embed=em)


  @commands.command(aliases=['lb'], description='Shows global leaderboards for coins and prestige. If you do not provide a type, the bot will send you the prestige leaderboard.', brief='Shows global leaderboards for coins and prestige.')
  async def leaderboard(self, ctx, *arg):

    if len(arg) == 0:

      data = await find_lb()
      
      

      for i in data:
        i['_id'] =  await self.bot.fetch_user(int(i['_id']))
      
      string = ''''''
      for x, i in enumerate(data, start=1):
        prestige = i['data']['prestige']
        name = str(i['_id']).strip('`')
        name2 = str(i['data']['name']).strip('`')
        string = string + f'**{x}.** {name}: `{name2}`| `Prestige Level {prestige}`\n'

      embed = discord.Embed(title='Global Leaderboard (prestige)', description=string)
      await ctx.send(embed=embed)

    elif len(arg) == 1:

      if arg[0] == 'coins':
        data = await find_lb2()
        
        

        for i in data:
          i['_id'] =  await self.bot.fetch_user(int(i['_id']))
        
        string = ''''''
        for x, i in enumerate(data, start=1):
          prestige = i['data']['coins']
          name = str(i['_id']).strip('`')
          name2 = str(i['data']['name']).strip('`')
          string = string + f'**{x}.** {name}: `{name2}`| `{prestige}` :coin:\n'

        embed = discord.Embed(title='Global Leaderboard (coins)', description=string)
        await ctx.send(embed=embed)

    else:
      await ctx.send(':x: uhhhhhh thats not not an option')

  @leaderboard.error
  async def lb_error(self, ctx, error):
    raise error


  @commands.command(description='Allows you to hunt for items and sell them for coins. The items go to your inventory', brief='Allows you to hunt for items and sell them for coins.')
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def hunt(self, ctx):
    try:
      a = await find_inventory(ctx.author.id)

    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Hey!', description=f'You dont have a country! Type `{prefix}start` to start your country!')
      await ctx.send(embed=embed)
      return

    lst = list(hunt_animals.keys())
    lst.append(' ')
    animal = random.choice(lst)

    if animal == ' ':
      embed = discord.Embed(title='Hunting', description='While hunting you found nothing :C')

      await ctx.send(embed=embed)

    else:
      embed = discord.Embed(title='Hunting', description=f"While hunting you found an {hunt_animals[animal][0]} {animal} worth {hunt_animals[animal][1]}")

      await ctx.send(embed=embed)

      if f'{hunt_animals[animal][0]} {animal}' not in a.keys():
        a[f'{hunt_animals[animal][0]} {animal}'] = {'amount': 1, 'value': hunt_animals[animal][1]}

      else:
        a[f'{hunt_animals[animal][0]} {animal}'] = {'amount': a[f'{hunt_animals[animal][0]} {animal}']['amount'] + 1, 'value': a[f'{hunt_animals[animal][0]} {animal}']['value'] + hunt_animals[animal][1]}

      await update_inventory((ctx.author.id, a))

      

  @hunt.error
  async def hunt_error(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
          em = discord.Embed(title="Hey!",description=f'''You can't hunt right now! Try again in `{error.retry_after:.2f}`s.''')
          await ctx.send(embed=em) 

  @commands.command(description='Sell items in your inventory', brief='Sell items in your inventory')
  async def sell(self, ctx, item, *amount):
    
    try:
      a = await find_inventory(ctx.author.id)
      ab = await reading(ctx.author.id)

    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Hey!', description=f'You dont have a country! Type `{prefix}start` to start your country!')
      await ctx.send(embed=embed)
      return
    
    

    if not amount:
      item = None
      for i in a.keys():
        if item1[0].lower() in i:
          item = i

      if item == None:
        await ctx.send(":x: You don't own that!")
        return

      else:
        value = a[item]['value']
        if a[item]['amount'] == 1:
          del a[item]
          await update_inventory((ctx.author.id, a))

          await ctx.send(embed=discord.Embed(title='Success', description=f'Sold {item}'))

          await update_coins((ctx.author.id, ab[0][11] + value))

        else:
          value = a[item]['value']/a[item]['amount']
          a[item] = {'amount': a[item]['amount'] - 1, 'value': a[item]['value'] - value}
        
          await update_inventory((ctx.author.id, a))

          await ctx.send(embed=discord.Embed(title='Success', description=f'Sold {item}'))

          await update_coins((ctx.author.id, ab[0][11] + value))

    else:
      amount = amount[0].strip(',')
      try:
        amount = int(item1[1])
      except:
        await ctx.send(':x: That is not a valid amount')
        return
      if amount <= 0:
        await ctx.send(':x: That is not a valid amount')
        return
      
      item = None
      for i in a.keys():
        if item1[0].lower() in i:
          item = i

      if item == None:
        await ctx.send(":x: You don't own that!")
        return
      
      
      amount1 = a[item]['amount']



      if amount1 < amount:
        await ctx.send(":x: You don't have that much of this item")
        return

      value = a[item]['value']/a[item]['amount'] * amount
      if a[item]['amount'] - amount == 0:
        del a[item]
      else:
        a[item]['amount'] = a[item]['amount'] - amount 


      await update_inventory((ctx.author.id, a))

      await ctx.send(embed=discord.Embed(title='Success', description=f'Sold {item}'))

      await update_coins((ctx.author.id, ab[0][11] + value))



  



  @commands.command(aliases=['inv'], description='View your inventory', brief='View your inventory')
  async def inventory(self, ctx):
    try:
      a = await find_inventory(ctx.author.id)

    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Sorry', description=f''':x: You don't have a country. Type `{prefix}start` to start one''')
      await ctx.send(embed=embed)
      return

    
    string = ''''''
    for x, i in enumerate(a.items()):
      amount = i[1]['amount']
      value = i[1]['value']
      string = string + f'**{x + 1}.** {i[0]} | Amount: {amount} : Worth: {value}\n'

    if len(a) == 0:
      string = ":x: You don't have anything in your inventory. Buy things from the shop with coins!"

    embed = discord.Embed(title='Inventory', description=string)
    await ctx.send(embed=embed)



  @commands.command(description='Start your country!', brief='Start your country!')
  async def start(self, ctx):
    try:
      embed = discord.Embed(title="Hooray", description='''We are very excited for you to start your own country :tada:
      In the chat type the **name** of your soon to be country''', color=Color.teal())

      await ctx.channel.send(embed=embed)
      the_channel, the_author = ctx.channel, ctx.message.author

      def check(m):
        return m.channel == the_channel and m.author == the_author

      msg = await self.bot.wait_for('message', check=check, timeout=100)

      await writing((ctx.author.id, msg.content, 0, 1, "Mayor", 1, 0, 50000000, 0, 0, 0, 0, 0))

      await ctx.channel.send('Hooray, Country Created!!!!')
    except:
      embed = discord.Embed(title='Sorry', description=''':x: You already have a country.''')

      await ctx.channel.send(embed=embed)





  @commands.command(description="Check information about your country, or another person's country.", breif="Check information about your country, or another person's country.")
  async def profile(self, ctx, member: discord.Member=None):
    if member == None:
      id = ctx.author.id
      member = ctx.author

    else:
      id = member.id

    try:
      a = await reading(id)
      name = a[0][0]
      username = member.name 
      discriminator = member.discriminator

      username = username.replace(' ', '%20')
      
      amount12 = 36 + len(str(ctx.author.id))
      url = f'https://cbotdiscord.npcool.repl.co/{id}/{str(member.avatar_url)[amount12:][:-15]}/{str(username)}/{str(discriminator)}'
      embed = discord.Embed(title=f'''{name}''', url=url, description=f'''Population: `{"{:,}".format(a[0][1])}`
                      Multiplier: `{"{:,}".format(a[0][2])}`
                      Job: `{a[0][3]}`
                      Work Ethic: `{a[0][4]}`
                      Office: `{dic[a[0][4]]}`
                      Work Commands Issued: 
                      `{a[0][10]}`
                      Coins: {a[0][11]} :coin:
                      ''')
      
      
      embed.add_field(name='War', value=f'''Wars Played: `{a[0][7]}`
                      Wars Won: `{a[0][8]}`
                      Wars Lost: `{a[0][9]}`
                      ''')

      embed.add_field(name='Prestige', value=f'''Prestige Level: `{a[0][5]}`
                      Prestige Requirement `{a[0][6]}` population''')

    
      embed.set_thumbnail(url=member.avatar_url)
      
      if dic[a[0][4]] == "Mom's basement":
        embed.set_image(url='http://www.storefrontlife.com/wp-content/uploads/2013/01/Basement.jpg')
      elif dic[a[0][4]] == 'Apartment (with roomate)': 
        embed.set_image(url='https://res.cloudinary.com/hemcfvrk2/image/upload/c_lfill,g_xy_center,x_1516,y_615,w_1200,h_700,q_auto:eco,fl_lossy,f_auto/v1485383879/uhzs2wektoh0mb5rkual.jpg')
      
      elif dic[a[0][4]] == 'Mansion':
        embed.set_image(url='https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2013/08/26/100987825-121017_EJ_stone_mansion_0014r.600x400.jpg?v=1395082652')

      
      elif dic[a[0][4]] == 'Home Office':
        embed.set_image(url='https://cdn1.epicgames.com/ue/product/Screenshot/01B-1920x1080-6fd10f5c37639159b1d7a57a869aa3ed.png?resize=1&w=1600')

      elif dic[a[0][4]] == 'Space Base':
        embed.set_image(url='https://cdna.artstation.com/p/assets/images/images/000/630/350/large/jarek-kalwa-space-base.jpg?1429173581')

      try:
        embed.set_footer(text=f'Tax your citizens with `{db[str(ctx.guild.id)]}tax` to earn coins!')
      except:
        pass
      
      await ctx.channel.send(embed=embed)

    except:
      prefix = await get_prefix(ctx.guild.id)
      embed= discord.Embed(title='Sorry', description=f''':x: You or the person you are viewing don't have a country yet. Type {prefix}start to create your amazing country!!!''')

      await ctx.channel.send(embed=embed)
    

  @commands.command(aliases=['shop'], description='Shows you items you can purchase for your country', brief='Shows you items you can purchase for your country')
  async def store(self, ctx):
    prefix = await get_prefix(ctx.guild.id)
    try: 
      a = await reading(ctx.message.author.id)
    except:
      embed = discord.Embed(title='Whoops', description=f"You haven't started a country yet. Type `{prefix}start` to create your amazing country!!!!")
      await ctx.channel.send(embed=embed)
      return

    status = 'NOT OWNED'
    status2 = 'NOT OWNED'
    status3 = 'NOT OWNED'
    status4 = 'NOT OWNED'

    if dic[a[0][4]] == 'Apartment (with roomate)':
      status = 'OWNED'
    

    if dic[a[0][4]] == 'Home Office':
      status = 'OWNED'
      status2 = 'OWNED'
  

    if dic[a[0][4]] == 'Mansion':
      status = 'OWNED'
      status2 = 'OWNED'
      status3 = 'OWNED'
  

    if dic[a[0][4]] == 'Space Base':
      status = 'OWNED'
      status2 = 'OWNED'
      status3 = 'OWNED'
      status4 = 'OWNED'
    
    embed = discord.Embed(title='Store', description=f'''**1. Multiplier Boost `1` :zap: ID = 1**
    To buy this item type: `{prefix}buy 1 <amount>`
    Cost: 500 :coin:
    Increases your multiplier by 1
    
    **2. Apartment (with roomate) ID = `2` Status: [{status}]**
    To buy this item type: `{prefix}buy 2`

    Cost:  1000 :coin:
    
    Your work ethic becomes 2 
    
    
    3. **Home Office :homes:  ID = `3` Status: [{status2}]**
    To buy this item type: `{prefix}buy 3`

    Cost: 10,000 :coin:
    
    Your work ethic becomes 3 
    
    
    4. **Mansion :homes:  ID = `4` Status: [{status3}]**
    To buy this item type: `{prefix}buy 4`

    Cost: 50,000 :coin:
    
    Your work ethic becomes 5 
    
    5. **Space Base :crescent_moon:  ID = 5 Status: [{status4}]**
    To buy this item type: `{prefix}buy 5`

    Cost: 100,000 :coin:
    
    Your work ethic becomes 10 
    
    
    
    ''')
    

    
    await ctx.channel.send(embed=embed)



  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(description='Work and earn population for your country!', brief='Work and earn population for your country!')
  async def work(self, ctx):
    chance = random.randint(1, 10)
    try:
      a = await (reading(ctx.message.author.id))
    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Sorry', description=f":x: You haven't created a country yet. To create one type `{prefix}start`. Have fun with your amazing country!!!")
      await ctx.channel.send(embed=embed)
      return

    if a[0][1] > 30000000000000000000000000000000000:
      embed = discord.Embed(title='Woah!', description='You have the max amount of population even possible! You better prestige!')
      await ctx.channel.send(embed=embed)
      return
    if a[0][1] >= 100 and a[0][3] == 'Mayor':
      embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `State Senator`')
      await ctx.channel.send(embed=embed)
      await update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'State Senator', a[0][4], a[0][10]))
      a = await reading(ctx.message.author.id)

    elif a[0][1] >= 10000 and a[0][3] == 'State Senator':
      embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `Governor`')
      await ctx.channel.send(embed=embed)
      await update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'Governor', a[0][4], a[0][10]))
      a = await reading(ctx.message.author.id)

    elif a[0][1] >= 50000 and a[0][3] == 'Governor':
      embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `Senator`')
      await ctx.channel.send(embed=embed)
      await update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'Senator', a[0][4], a[0][10]))
      a = await reading(ctx.message.author.id)

    elif a[0][1] >= 200000 and a[0][3] == 'Senator':
      embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `Vice President`')

      await ctx.channel.send(embed=embed)
      await update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'Vice President', a[0][4], a[0][10]))
      a = await reading(ctx.message.author.id)

    elif a[0][1] >= 2500000 and a[0][3] == 'Vice President':
      embed = discord.Embed(title='Promotion!!!!', description=f'Congratulations!!, You have been promoted to `President` You are now the leader of {a[0][0]}')
      await ctx.channel.send(embed=embed)
      await update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'President', a[0][4], a[0][10]))
      a = await reading(ctx.message.author.id)


    
  
    
    
    try:
      if a[0][3] == 'Mayor':
        amount1 = random.randint(0, 5)
        amount1 = amount1 * a[0][4]
        if float(a[0][2]).is_integer():
          embed=discord.Embed(title='Boost Time!!!!! :zap:', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
          await ctx.channel.send(embed=embed)
          amount1 = amount1 * a[0][2]


        amount = amount1 + int(a[0][1])
        multi = float("{:.1f}".format(a[0][2] + (a[0][5] +1)/10))
        await update((ctx.message.author.id, a[0][0], amount,multi, 'Mayor', a[0][4], a[0][10] + 1))

        

        embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

        await ctx.channel.send(embed=embed)
        if chance == 5:
          a = await reading(ctx.message.author.id)
          await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
          embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
          await ctx.channel.send(embed=embed_chance)

      elif a[0][3] == 'State Senator':
        amount1 = random.randint(50, 100)
        amount1 = amount1 * a[0][4]
        if float(a[0][2]).is_integer():
          embed=discord.Embed(title='Boost Time!!!!! :zap:', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
          await ctx.channel.send(embed=embed)
          amount1 = amount1 * a[0][2]


        amount = amount1 + int(a[0][1])
        multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
        await update((ctx.message.author.id, a[0][0], amount,multi, 'State Senator', a[0][4], a[0][10] + 1))

        embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

        await ctx.channel.send(embed=embed)
        if chance ==  5:
          a = await reading(ctx.message.author.id)
          await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
          embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
          await ctx.channel.send(embed=embed_chance)

      elif a[0][3] == 'Governor':
        amount1 = random.randint(100, 500)
        amount1 = amount1 * a[0][4]
        if float(a[0][2]).is_integer():
          embed=discord.Embed(title='Boost Time!!!!! :zap:', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
          await ctx.channel.send(embed=embed)
          amount1 = amount1 * a[0][2]

        

        amount = amount1 + int(a[0][1])
        multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
        await update((ctx.message.author.id, a[0][0], amount,multi, 'Governor', a[0][4], a[0][10] + 1))

        embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

        await ctx.channel.send(embed=embed)
        if chance == 5:
          a = await reading(ctx.message.author.id)
          await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
          embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
          await ctx.channel.send(embed=embed_chance)

      elif a[0][3] == 'Senator':
        amount1 = random.randint(1000, 5000)
        amount1 = amount1 * a[0][4]

        if float(a[0][2]).is_integer():
          embed=discord.Embed(title='Boost Time :zap:!!!!!', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
          await ctx.channel.send(embed=embed)
          amount1 = amount1 * a[0][2]
        amount = amount1 + int(a[0][1])
        multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
        await update((ctx.message.author.id, a[0][0], amount,multi, 'Senator', a[0][4], a[0][10] + 1))

        embed = discord.Embed(title='Work Work Work :zap:!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

        await ctx.channel.send(embed=embed)
        if chance == 5:
          a = await reading(ctx.message.author.id)
          await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
          embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
          await ctx.channel.send(embed=embed_chance)

      elif a[0][3] == 'Vice President':
        amount1 = random.randint(10000, 50000)
        amount1 = amount1 * a[0][4]
        if float(a[0][2]).is_integer():
          embed=discord.Embed(title='Boost Time :zap:!!!!!', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
          await ctx.channel.send(embed=embed)
          amount1 = amount1 * a[0][2]


        amount = amount1 + int(a[0][1])
        multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
        await update((ctx.message.author.id, a[0][0], amount,multi, 'Vice President', a[0][4], a[0][10] + 1))

        embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

        await ctx.channel.send(embed=embed)
        if chance == 5:
          a = await reading(ctx.message.author.id)
          await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
          embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
          await ctx.channel.send(embed=embed_chance)

      elif a[0][3] == 'President':
        amount1 = random.randint(50000, 100000)
        amount1 = amount1 * a[0][4]
        if float(a[0][2]).is_integer():
          embed=discord.Embed(title='Boost Time!!!!! :zap:', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
          await ctx.channel.send(embed=embed)
          amount1 = amount1 * a[0][2]
        amount = amount1 + int(a[0][1])
        multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
        await update((ctx.message.author.id, a[0][0], amount,multi, 'President', a[0][4], a[0][10] + 1))

        embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

        await ctx.channel.send(embed=embed)
        if chance == 5:
          a = await reading(ctx.message.author.id)
          await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
          embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
          await ctx.channel.send(embed=embed_chance)
    
    
    except OverflowError:
      await ctx.send(" :x: You have WAY too much population. You better prestige or you won't be able to work!")

  @work.error
  async def work_error(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
          em = discord.Embed(title="Too tired",description=f'''You are too tired to work again. You can work in `{error.retry_after:.2f}`s.''')
          await ctx.send(embed=em)

      


  @commands.command(description='Prestige your country. This means that your population and multiplier will be reset, but you earn more coins, more multiplier and more population.', brief='Prestige your country.')
  async def prestige(self, ctx):
    try:
      a = await reading(ctx.message.author.id)
    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Sorry', description=f":x: You haven't created a country yet. To create one type `{prefix}start`. Have fun with your amazing country!!!")
      await ctx.channel.send(embed=embed)
      return
    

    
    if a[0][1] > a[0][6]:
      embed = discord.Embed(title='Hooray!!', description='You have met the requirements to prestige!! Do you want to prestige `y` | `n`')
      await ctx.channel.send(embed=embed)
      def check(m):
        return m.channel == ctx.channel and m.author == ctx.message.author

      try:
          msg = await self.bot.wait_for('message', check=check, timeout=100)

          if msg.content.lower() == 'n':
            embed = discord.Embed(title='ok', description=':x: Prestige cancelled')
            await ctx.channel.send(embed=embed)
            

          elif msg.content.lower() == 'y':
            await update_prestige((ctx.message.author.id, a[0][0], 0, 1, 'Mayor', 1, a[0][5] + 1, (a[0][6] + 50000000)))
            embed = discord.Embed(title='Congratulations', description=':tada: You prestiged!!')
            await ctx.channel.send(embed=embed)
            
          else:
            await ctx.send('That isnt a valid option!')
      except asyncio.TimeoutError:
          await ctx.send('Time ran out :C')
        
        
    else:
      embed = discord.Embed(title='Oh No', description=''':x: you haven't met the requirements to prestige''')
      await ctx.channel.send(embed=embed)
      
  @commands.command(description='Deletes your country :((', brief='Deletes your country :((')
  async def quit(self, ctx):
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='quit', description=':x: Are you really sure you want to quit your country. You will lose all your data (`y`,`n`)')
    await ctx.channel.send(embed=embed)
    thechannel = ctx.channel
    theauthor = ctx.message.author
    def check(m):
      return m.content == 'y' or m.content == 'n' and m.channel == thechannel and m.author == theauthor 
    msg = await self.bot.wait_for('message', check=check, timeout=100)
    try:
      a = await reading(ctx.message.author.id)
      if msg.content == 'y':
        await delete_task(ctx.message.author.id)
        embed = discord.Embed(title="Country deleted", description=f"Your country is gone, and you can't become the leader :cry:. But don't worry :D. You can start a new one with `{prefix}start`")
        await ctx.channel.send(embed=embed)
      elif msg.content == 'n':
        embed = discord.Embed(title='Phew', description=f'Your country is not deleted :DD')
        await ctx.channel.send(embed=embed)
    except:
      embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{prefix}start`''')
      await ctx.channel.send(embed=embed)


  @commands.command(description='Buy items for your country!', brief='Buy items for your country!')
  async def buy(self, ctx, id, *amount):
    prefix = await get_prefix(ctx.guild.id)
    try:
      a = await reading(ctx.message.author.id)
    except:
      
      embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{prefix}start`''')
      await ctx.channel.send(embed=embed)

    
    if len(amount) == 1:
      amount = amount[0]
      amount = amount.strip(',')

      try:
        int(amount)
      except:
        await ctx.send(':x: uhhhh. Thats not a valid amount')

      

      if id == '1':
          if a[0][11] - (500 * int(amount)) < 0:
            embed = discord.Embed(title='Oh no', description=''':x: You don't have enough coins!''')
            await ctx.channel.send(embed=embed)
            return

          if a[0][2] > 10000000:
            embed = discord.Embed(title='Stop!', description="You can't buy anymore multiplier!!")
            await ctx.channel.send(embed=embed)
            return

          if int(amount) <= 0:
            await ctx.send(":x: You can't buy this amount of multiplier smh")
            return
          if (int(amount)) + a[0][2] > 10000000:
            embed = discord.Embed(title='Stop!', description="You can't buy anymore multiplier!!")
            await ctx.channel.send(embed=embed)
            return

          await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + (1 * int(amount)), a[0][3], a[0][4], a[0][10]))

          await update_coins((ctx.author.id, a[0][11] - (500 * int(amount))))

          embed = discord.Embed(title='Congratulations',
            description=f'You have bought {amount} Multiplier Boosts')
          await ctx.channel.send(embed=embed)

        

        

    elif len(amount) == 0:
    
      if id == '1':
        embed = discord.Embed(title='Error', description=':x: How much multipliere are you buying!')
        await ctx.channel.send(embed=embed)

      elif id == '2':
        if a[0][4] >= 2:
          embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
          await ctx.channel.send(embed=embed)
          return
        if (a[0][11] - 1000) < 0:
          embed = discord.Embed(title='Oh no', description=''':x: You don't have enough coins!''')
          await ctx.channel.send(embed=embed)
          return

        
        await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2], a[0][3], (a[0][4] + 1), a[0][10]))

        await update_coins((ctx.author.id, a[0][11] - 1000))

        embed = discord.Embed(title='Congratulations',
          description=f'You have bought the Apartment (with roomate)')
        await ctx.channel.send(embed=embed)

      elif id == '3':
        if a[0][4] >= 3:
          embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
          await ctx.channel.send(embed=embed)
          return
        elif a[0][4] < 2:
          embed = discord.Embed(title='Hey', description=':x: You need to buy the apartment first!!!')
          await ctx.channel.send(embed=embed)
          return
        if (a[0][11] - 10000) < 0:
          embed = discord.Embed(title='Oh no', description=''':x: You don't have enough coins!''')
          await ctx.channel.send(embed=embed)
          return

        
        await update((ctx.message.author.id, a[0][0], a[0][1] , a[0][2], a[0][3], (a[0][4] + 1), a[0][10]))

        await update_coins((ctx.author.id, a[0][11] - 10000))

        embed = discord.Embed(title='Congratulations',
          description=f'You have bought the Home Office')
        await ctx.channel.send(embed=embed)

      elif id == '4':
        if a[0][4] >= 5:
          embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
          await ctx.channel.send(embed=embed)
          return
        if a[0][4] < 3:
          embed = discord.Embed(title='Hey', description=':x: You need to buy the Home Office first!!!')
          await ctx.channel.send(embed=embed)
          return
        if (a[0][11] - 50000) < 0:
          embed = discord.Embed(title='Oh no', description=''':x: You don't have enough coins!''')
          await ctx.channel.send(embed=embed)
          return

        
        await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2], a[0][3], (a[0][4] + 2), a[0][10]))

        await update_coins((ctx.author.id, a[0][11] - 50000))

        embed = discord.Embed(title='Congratulations',
          description=f'You have bought the Mansion')
        await ctx.channel.send(embed=embed)
      
      elif id == '5':
        if a[0][4] >= 10:
          embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
          await ctx.channel.send(embed=embed)
          return
        if a[0][4] < 5:
          embed = discord.Embed(title='Hey', description=':x: You need to buy the Mansion first!!!')
          await ctx.channel.send(embed=embed)
          return
        if (a[0][11] - 100000) < 0:
          embed = discord.Embed(title='Oh no', description=''':x: You don't have enough coins!''')
          await ctx.channel.send(embed=embed)
          return

        
        await update((ctx.message.author.id, a[0][0], a[0][1], a[0][2], a[0][3], (a[0][4] + 5), a[0][10]))

        await update_coins((ctx.author.id, a[0][11] - 100000))



        embed = discord.Embed(title='Congratulations',
          description=f'You have bought the Space Base')
        await ctx.channel.send(embed=embed)


      else:
        embed = discord.Embed(title='ummmm', description="This ID doesn't exist. Check out the shop command to see all the available IDs")
        await ctx.send(embed=embed)

 

  @commands.command(description='Gift some population to other people!', brief='Gift some population to other people!')
  async def gift(self, ctx, user, amount):
    user1 = user
    try:
      b = user1.replace("<","")
      b = b.replace(">","")
      b = b.replace("@","")
      user = b.replace("!", "")

      

      a = await reading(user)

    except:
      embed = discord.Embed(title='Whoops', description=':x: This person doesnt have a country!!')
      await ctx.channel.send(embed=embed)
      return

  

    if str(user) == str(ctx.message.author.id):
        embed=discord.Embed(title='Hey!', description=":x: You can't give gifts to yourself!")
        await ctx.channel.send(embed=embed)
        return

    try:
      b = await reading(ctx.author.id)

    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Whoops', description=f":x: You don't have a country!! Type `{prefix}start` to start your country!")
      await ctx.channel.send(embed=embed)
      return

    try:

      amount = amount.strip(',')
      if amount.isnumeric():
        if int(amount) > b[0][1]:
          embed = discord.Embed(title="Hey!", description=":x: You don't have that many people!")
          await ctx.channel.send(embed=embed)
          return

        else:
            await update((ctx.author.id, b[0][0], b[0][1] - int(amount), b[0][2], b[0][3], b[0][4], b[0][10]))

            await update((user, a[0][0], a[0][1] + int(amount), a[0][2], a[0][3], a[0][4], a[0][10]))

            await ctx.channel.send(embed=discord.Embed(title="Success!", description=f"Succesfully transefered {amount} people to {user1}'s country!"))
        
      else:
        
        if amount.lower() == 'half':
            await update((ctx.author.id, b[0][0], int(b[0][1]/2), b[0][2], b[0][3], b[0][4], b[0][10]))

            await update((user, a[0][0], a[0][1] + int(b[0][1]/2), a[0][2], a[0][3], a[0][4], a[0][10]))

            await ctx.channel.send(embed=discord.Embed(title="Success!", description=f"Succesfully transefered {int(b[0][1]/2)} people to {user1}'s country!"))

            return

        elif amount.lower() == 'all':
            await update((ctx.author.id, b[0][0], 0, b[0][2], b[0][3], b[0][4], b[0][10]))

            await update((user, a[0][0], a[0][1] + b[0][1], a[0][2], a[0][3], a[0][4], a[0][10]))

            await ctx.channel.send(embed=discord.Embed(title="Success!", description=f"Succesfully transefered {int(b[0][1])} people to {user1}'s country!"))

            return
        embed = discord.Embed(title='Hey!', description=":x: That is not a valid amount!")
        await ctx.channel.send(embed=embed)
    except OverflowError:
      await ctx.send(":x: You can't gift that much at a time")

      

    

    

  @commands.command(description='Change your country name!', brief='Change your country name!')
  async def change(self, ctx, *, name):
    arg = name
    try:
      a = await reading(ctx.message.author.id)
    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{prefix}start`''')
      await ctx.channel.send(embed=embed)

    if len(arg) > 50:
      embed = discord.Embed(title='Hey!', description=':x: The name can only be up to 50 characters')
      await ctx.channel.send(embed=embed)
      return

    arg = arg.replace("'", "`")
    await update((ctx.message.author.id, arg, a[0][1], a[0][2], a[0][3], a[0][4], a[0][10]))
    embed = discord.Embed(title='Success', description=f'Country name Has been succesfully changed to {arg}')

    await ctx.channel.send(embed=embed)


  @commands.cooldown(1, 86400, commands.BucketType.user)
  @commands.command(description='Get your daily allowance of population...', brief='Get your daily allowance of population...')
  async def daily(self, ctx):
    try:
      a = await reading(ctx.message.author.id)
    except:
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{prefix}start`''')
      
    a = await reading(ctx.message.author.id)
    await update((ctx.message.author.id, a[0][0], a[0][1] + int((100 * (((a[0][1]**0.5)/100)) * (a[0][5] +1))), a[0][2], a[0][3], a[0][4], a[0][10]))

    

    embed = discord.Embed(title='Daily', description=f'`{int((100 * ((a[0][1]**0.5)/100)) * (a[0][5] +1))}` more people joined your country!! Your new population is `{a[0][1] + int((100 * ((a[0][1]**0.5)/100)) * (a[0][5] +1))}`')

    await ctx.channel.send(embed=embed)

  @daily.error
  async def daily_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
            time1 = error.retry_after
            em = discord.Embed(title="Slow it down!",description=f'''Try again after `{datetime.timedelta(seconds = time1)}`.''')
            await ctx.send(embed=em)







class Games(commands.Cog, description='Cool games that test your geography skills'):
  def __init__(self, bot):
    self.bot = bot

  
  @commands.command(cooldown_after_parsing=True, description='Wage war on your friends!', brief='Wage war on your friends!')
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def war(self, ctx, user: discord.Member):
    b = user.id

    opponent = user
    

    
    
    
      
    if int(b) == int(ctx.author.id):
        embed = discord.Embed(title='Stop!', description=":x: You can't wage war on yourself!")
        await ctx.channel.send(embed=embed)
        return
    

      
    try:
      user1 = await reading(ctx.message.author.id)
    except:
      prefix = await get_prefix(ctx.guild.id)
      embed= discord.Embed(title='Sorry', description=f''':x: You don't have a country yet. Type {prefix}start to create your amazing country!!!''')

      await ctx.channel.send(embed=embed)
      return
    try:
      user2 = await reading(b)
    except:
      embed= discord.Embed(title='Sorry', description=f''':x: This user doesn't have a country yet''')

      await ctx.channel.send(embed=embed)
      return

    if user1[0][1] == 0 or user2[0][1] == 0:
      await ctx.send(":x: Hey! One of you has only 0 population! You can't go to war like that smh")
      return
    
    await ctx.channel.send(f"<@!{b}>, you have 20 seconds to accept <@!{ctx.message.author.id}> request to war. Type `accept` in the chat to accept, or type `deny` in the chat to end the conflict")

    
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
        
        if num <= 0:
          await ctx.channel.send("You can't go to war with less than 0 people smh")
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

        if num <= 0:
          await ctx.channel.send("You can't go to war with less than 0 people smh")
          continue
      except:
        if msg.content.lower() == 'quit':
          await ctx.send(':x: Game Quit')
          return
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
        await update_war((ctx.message.author.id, user1[0][0], user1[0][1] + user2_troops, user1[0][2], user1[0][3], user1[0][4], user1[0][5], user1[0][6], user1[0][7] + 1, user1[0][8] + 1, user1[0][9]))

        await update_war((b, user2[0][0], user2[0][1] - user2_troops, user2[0][2], user2[0][3], user2[0][4], user2[0][5], user2[0][6], user2[0][7] + 1, user2[0][8], user2[0][9] + 1))
      
    else:
        await ctx.channel.send(f'{user} you gave the answer first. You won the war!!! :crown:')
        await update_war((ctx.message.author.id, user1[0][0], user1[0][1] - user1_troops, user1[0][2], user1[0][3], user1[0][4], user1[0][5], user1[0][6], user1[0][7] + 1, user1[0][8], user1[0][9] + 1))

        await update_war((b, user2[0][0], user2[0][1] + user1_troops, user2[0][2], user2[0][3], user2[0][4], user2[0][5], user2[0][6], user2[0][7] + 1, user2[0][8] + 1, user2[0][9]))



  @war.error
  async def war_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title="Hey!",description=f'''You can't wage war right now! Try again in `{error.retry_after:.2f}`s.''')
      await ctx.send(embed=em)



  @commands.command(description='Guess capitals of countries, or guess countries from their capitals!', brief='Guess capitals of countries, or guess countries from their capitals!')
  async def guess_capital(self, ctx, *reverse):
      arg = reverse
      the_author = ctx.message.author
      channel = ctx.message.channel

      await ctx.channel.send("How long should the time limit be (**in seconds**)")

      def check1(m):
        return m.content.isdigit() and m.author == the_author and m.channel == channel and int(m.content) <= 300

      msg1 = await self.bot.wait_for("message", check=check1)

      length = int(msg1.content)

      
      correct_ans = {}

      

      if len(arg) == 0 or len(arg) >= 1 and arg[0].lower() != 'reverse':
        count = 0
        bol = True
        while bol:
          random_country = random.choice(quiz_country_list)
          try:
            country_capital1 = CountryInfo(random_country)
            
            country_capital = country_capital1.capital()
          except:
            random_country = random.choice(quiz_country_list)
            country_capital1 = CountryInfo(random_country)
            
            country_capital = country_capital1.capital()

          if not country_capital:
            try:
              random_country = random.choice(quiz_country_list)
              country_capital1 = CountryInfo(random_country)

              country_capital = country_capital1.capital()
            except:
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
            return fuzz.ratio(country_capital.lower(), m.content.lower()) > 85 or m.content.lower() == 'quit' and m.channel == channel

          try:
            msg = await self.bot.wait_for('message', check=check, timeout=length)

            if msg.content == 'quit':
              await ctx.channel.send("Game Over")
              break

            count += 1

            if msg.author.id not in correct_ans:
              correct_ans[msg.author.id] = 1

            else:
              correct_ans[msg.author.id] += 1

            await ctx.channel.send(f"That is the correct answer!!! 🏆 Good Job <@{msg.author.id}>")
            
            bol = True

          except asyncio.TimeoutError:
            try:
              await ctx.channel.send(f'''Time has run out!! ***Game Over***. Total score: `{count}` 
    The highest scorer in this match was <@{max(correct_ans, key=lambda key: correct_ans[key])}> with a score of `{correct_ans[msg.author.id]}` GG''')
              break 
            except:
              await ctx.channel.send("No one scored in this match. :cry: Total score `0`")
              break

          

      elif len(arg) == 1 and arg[0].lower() == 'reverse':
        count = 0
        bol = True
        while bol:

          random_country = random.choice(quiz_country_list)

          country_capital1 = CountryInfo(random_country)

          country_capital = country_capital1.capital()

          

          result4 = coco.convert(names=random_country, to='ISO2')

          await ctx.channel.send(f"What Country has `{country_capital.title()}` as its capital. Here is a hint: {lookup(result4)}")

        

          

          def check(m):
            return fuzz.ratio(random_country.lower(), m.content.lower()) > 82 and m.channel == channel

          try:
            msg = await self.bot.wait_for('message', check=check, timeout=length)

            count += 1

            if msg.author.id not in correct_ans:
              correct_ans[msg.author.id] = 1

            else:
              correct_ans[msg.author.id] += 1

            await ctx.channel.send(f"That is the correct answer!!! 🏆 Good Job <@{msg.author.id}>")
            
            bol = True

          except asyncio.TimeoutError:
            try:
              await ctx.channel.send(f'''Time has run out!! ***Game Over***. Total score: `{count}` 
    The highest scorer in this match was <@{max(correct_ans, key=lambda key: correct_ans[key])}> with a score of `{correct_ans[msg.author.id]}` GG''')
              break 
            except:
              await ctx.channel.send("No one scored in this match. :cry: Total score `0`")
              break


          




  




def setup(bot):
  bot.add_cog(EconomyCommands(bot))
  bot.add_cog(Games(bot))