#importing dependecies
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import inspect
import pymongo, dns
from mongomethods import user_exists
import discord
from mongomethods import count, reading, update, update_prestige, update_war, writing, delete_task, search_name, update_coins, find_inventory
import textwrap, contextlib
from traceback import format_exception
from discord.ext import tasks
from discord import Color
import regex as re
import keep_alive
import urllib
import io
from discord_slash import SlashCommand, SlashContext
import os
from pathlib import Path
import motor.motor_asyncio
from countryinfo import CountryInfo
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import country_converter as coco
import pycountry
import datetime
import requests
import json
import wbdata
import random
import time
import unicodedata
from help_page import geographical, economy, general, country_database, admin_stuff, games, misc, gambling, developer_commands
global cc
import resource, psutil
from replit import db
from fuzzywuzzy import fuzz
import asyncio, os
import operator
from emojiflags.lookup import lookup


global main_url

global quiz_country_list
quiz_country_list = list(CountryInfo().all().keys())

main_url = 'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'




# Find the document

#client1 = pymongo.MongoClient(os.environ['MONGO'])

#db1 = client1.db_name

#my_collection = db1.collection_name

#my_collection.update_many({}, {'$set': {"inventory": {}}})


#my_collection.insert_many([{"_id": str(i[0]), "data": {"name": i[1], "population": i[2], "multiplier": i[3], "job": i[4], "work_ethic": i[5], "prestige": i[6], "requirement": i[7], "wars_played": i[8], "wars_won": i[9], "wars_lost": i[10], "times_worked": i[11]}} for i in reading2()])






#getting the prefix of the guild from the JSON file
def get_prefix(bot, msg):
    if not msg.guild:
      return '.'
      
    else:
      prefixes = db[str(msg.guild.id)]
      return prefixes

   
  

global dic
dic = {1 : "Mom's basement", 2 : 'Apartment (with roomate)', 3 : 'Home Office', 5 : 'Mansion', 10 : 'Space Base'}


#Initiating flask app



#initiating country_converter
cc = coco.CountryConverter()

global username, password, userAgent

username = os.environ['USERNAME']
password = os.environ['PASSWORD']

userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'




bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, help_command=None)



global main_up
main_up = time.time()

data = {
  'client_id': int(os.environ['CLIENTID']),
  'client_secret': os.environ['CLIENTSECRET']
}



slash = SlashCommand(bot, sync_commands=True)

@slash.slash(name="test", guild_ids=[821872779523522580])
async def _test(ctx: SlashContext):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])




#add guild.id to JSON file on guild join

@bot.event
async def on_guild_join(guild):
  db[guild.id] = '.'
  
  

 

#remove guild.id from JSON file on guild remove
@bot.event
async def on_guild_remove(guild):
  del db[guild.id]
  

 
  
#A command to change the prefix of the bot in that guild



def start_extensions(bot):
  bot.load_extension("extensions.adminstuff")
  bot.load_extension("extensions.topgg")
  bot.load_extension("extensions.misc")
  bot.load_extension("extensions.country_database")
  bot.load_extension("extensions.gambling")
  bot.load_extension("extensions.economy")





@bot.command()
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

  
  tax1 = round(a[0][1] ** 0.5) * a[0][5] + 1

  await ctx.send(embed=discord.Embed(title='Tax', description=f'You got {tax1} :coin: from taxing your population'))

  update_coins((ctx.author.id, tax1 + a[0][11]))

@tax.error
async def tax_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="Hey!",description=f'''You can't collect taxes now! Try again in `{error.retry_after:.2f}`s.''')
        await ctx.send(embed=em)

@bot.command()
async def inventory(ctx):
  try:
    a = find_inventory(ctx.author.id)

  except:
    embed = discord.Embed(title='Sorry', description=f''':x: You don't have a country. Type `{db[str(ctx.guild.id)]}start` to start one''')
    await ctx.send(embed=embed)
    return

  
  string = ''''''

  for x, i in enumerate(a.items()):
    string = string + f'**{x}.** {i[0]}: {i[1]}'

  if len(a) == 0:
    string = ":x: You don't have anything in your inventory. Buy things from the shop with coins!"

  embed = discord.Embed(title='Inventory', description=string)
  await ctx.send(embed=embed)



@bot.command()
async def profile_name(ctx, name):
  try:
      a = search_name(name)
      name = a[0][0]
      
      embed = discord.Embed(title=f'''{name}''', description=f'''Population: `{"{:,}".format(a[0][1])}`
                      Multiplier: `{"{:,}".format(a[0][2])}`
                      Job: `{a[0][3]}`
                      Work Ethic: `{a[0][4]}`
                      Office: `{dic[a[0][4]]}`
                      Work Commands Issued: 
                      `{a[0][10]}`
                      {a[0][11]} :coin:
                     ''')
      
      
      embed.add_field(name='War', value=f'''Wars Played: `{a[0][7]}`
                      Wars Won: `{a[0][8]}`
                      Wars Lost: `{a[0][9]}`
                      ''')

      embed.add_field(name='Prestige', value=f'''Prestige Level: `{a[0][5]}`
                      Prestige Requirement `{a[0][6]}` population''')

      embed.set_thumbnail(url=ctx.author.avatar_url)
      if dic[a[0][4]] == "Mom's basement":
        embed.set_image(url='http://www.storefrontlife.com/wp-content/uploads/2013/01/Basement.jpg')
      elif dic[a[0][4]] == 'Apartment (with roomate)': 
        embed.set_image(url='https://res.cloudinary.com/hemcfvrk2/image/upload/c_lfill,g_xy_center,x_1516,y_615,w_1200,h_700,q_auto:eco,fl_lossy,f_auto/v1485383879/uhzs2wektoh0mb5rkual.jpg')
      
      elif dic[a[0][4]] == 'Mansion':
        embed.set_image(url='https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2013/08/26/100987825-121017_EJ_stone_mansion_0014r.600x400.jpg?v=1395082652')

      
      elif dic[a[0][4]] == 'Home Office':
        embed.set_image(url='https://blog-www.pods.com/wp-content/uploads/2020/07/Feature-Home-Office-GEtty-Resized.jpg')

      elif dic[a[0][4]] == 'Space Base':
        embed.set_image(url='https://cdna.artstation.com/p/assets/images/images/000/630/350/large/jarek-kalwa-space-base.jpg?1429173581')
      
      await ctx.channel.send(embed=embed)
  except:
      embed = discord.Embed(title='Sorry', description=f''':x: There is no country with this name''')
      await ctx.send(embed=embed)



  #command to get information about the bot


@bot.command()
async def flag(ctx, *country: str):
  if len(country) == 0:
    country = random.choice(quiz_country_list)
    result4 = coco.convert(names=country, to='ISO2')
    url = f'https://flagcdn.com/w320/{result4.lower()}.jpg'
    e = discord.Embed(title=f'Flag of {country.title()}')
    e.set_image(url=url)
    await ctx.send(embed=e)
  else:
    country = ' '.join(country)
    
    result4 = coco.convert(names=country, to='ISO2')
    
    
    url = f'https://flagcdn.com/w320/{result4.lower()}.jpg'
    e = discord.Embed(title=f'Flag of {country.title()}')
    e.set_image(url=url)
    try:
      await ctx.send(embed=e)
    except:
      embed = discord.Embed(title='Error', description=':x: Country not found')
      await ctx.send(embed=embed)
      
    

@bot.command()
async def war(ctx, user):
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
    msg = await bot.wait_for('message', check=check, timeout=20)
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
      msg = await bot.wait_for('message', check=check, timeout=20)
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
      msg = await bot.wait_for('message', check=check, timeout=20)
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
    msg = await bot.wait_for('message', check=check, timeout=30)
    
    
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
  

@bot.command()
async def stats(ctx):
  current_process = psutil.Process()
  cpu_usage = current_process.cpu_percent()
  memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000
  current_time = time.time()
  difference = int(round(current_time - main_up))
  text = str(datetime.timedelta(seconds=difference))
  
  embed = discord.Embed(title="Stats", color = Color.teal())

  
  embed.add_field(name='Server Count', value=f'''```css
[{len(bot.guilds)} servers]
```''')

  embed.add_field(name='CPU usage', value=f'''```css
[{cpu_usage}%]
```''', inline=True)
  
  embed.add_field(name='Uptime', value=f'''```css
[{text}]
```''')
  embed.add_field(name='Memory', value=f'''```ini
[{memory} kb]
```''')
  
  embed.add_field(name='User Countries', value=f'''```ini
[{count()}]
```''')

  embed.add_field(name='Creator', value=f'''```ini
[Coder N#0659]
```''', inline=True)

  embed.add_field(name='Ping', value=f'''```ini
[{bot.latency * 1000} ms]
```''')

  embed.add_field(name='Commands', value=f'''```css
[{len(bot.commands)}]
```''')




  embed.set_footer(text='If some percentages show 0.0%, it means that the number is really close to zero.')
  await ctx.channel.send(embed=embed)


@bot.command()
async def ping(ctx):
  embed = discord.Embed(title='Pong', description=f'''```ini
[{bot.latency * 1000} ms]
```''')

  await ctx.channel.send(embed=embed)
async def presence():
  while True:
      await bot.change_presence(activity=discord.Game(name=".help"))
      await asyncio.sleep(10)
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="@Country Bot prefix"))
      await asyncio.sleep(10)




@bot.command()
async def drake(ctx, *, arg):
  data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
  images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
  
  arg = arg.split('|')
  URL = 'https://api.imgflip.com/caption_image'
  params = {
      'username':username,
      'password':password,
      'template_id': images[0]['id'],
      'text0':arg[1],
      'text1': arg[2]
  }
  response = requests.request('POST',URL,params=params).json()
  
  url = response['data']['url']

  embed = discord.Embed(title=arg[0])
  embed.set_image(url=url)

  await ctx.send(embed=embed)

  



  

    
@bot.command()
async def changelog(ctx):
  embed = discord.Embed(title='Changelog', description='''**1.** Added new `.meme` feature
  **2.** New `.coinflip` feature
  **3.** Added statistics for `work commands issued`
  **4.** Added Statistics for `war` on country profiles
  **5.** Added a special feature only in the support server
  **6.** Added new feature `.gift` (allows you to gift population to other users
  **7.** New autocorrect when you misspell a command''')
  await ctx.send(embed=embed)


#setting the status of the bot and sending a message if the guild is not in db

async def refugee_drops():


  words = ['come here!', 'more people!', ':-D', "hello!"]

 

  channel = await bot.fetch_channel( 836624980359643176)

  while True:
      word = random.choice(words)
      amount = random.randint(100, 1000)
      
      message = await channel.send(embed=discord.Embed(title='Refugees', description=f'{amount} refugees have showed up. Who will be the first person to bring them in! Say `{word}` to bring them in!!'))

      def check(m):
        return m.content == word and m.channel == channel
      n = True
      while n:
        try:
          msg = await bot.wait_for('message', check=check, timeout = 30)

          try: 
            a = reading(msg.author.id)
          except:
            embed = discord.Embed(title='Sorry', description=":x: You don't have a country. Type `.start` to start one")
            await msg.channel.send(embed=embed)
            n = True

          update((msg.author.id, a[0][0], a[0][1] + amount, a[0][2], a[0][3], a[0][4], a[0][10]))
          await msg.reply(embed=discord.Embed(title='Hooray', description=f'{amount} more people added to your country!'))

          break


        except asyncio.TimeoutError:
          await message.delete()
          break

      await asyncio.sleep(300)

@bot.command(name="eval", aliases=["exec"])
async def _eval(ctx, *, code):

  if ctx.author.id == 751594192739893298:
    code = code.strip('```py')
    code = code.strip('```Python')
    code = code.strip('```python')
    
    

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
            )

            obj = await local_variables["func"]()
            result = f"```py\n{stdout.getvalue()}\n-- {obj}\n```"
    except Exception as e:
        result = f"```py\n{e}```"

    await ctx.send(embed=discord.Embed(description=f'''{result}'''))

  else:
    embed = discord.Embed(title='Hey!', description=":x: You don't have permission to use this command!")
    await ctx.send(embed=embed)


      
@bot.event
async def on_ready():  
    global task
    task = bot.loop.create_task(refugee_drops())
    bot.loop.create_task(presence())
    for i in bot.guilds:
      if str(i.id) not in db:
        for channel in i.channels:
            if channel.type == discord.ChannelType.text:
              main_channel =  bot.get_channel(channel.id)
              print('OfflINE')
              try:
                await main_channel.send("To continue using this bot, please `kick` it and `add it again`. This could have been caused because the `bot was added when it was offline`.")
                break
              except:
                pass
      
          
    

    print('bot is ready')
    print(f"bot is in {len(bot.guilds)} servers")

#commands for the bot


#listening for the message that users send if they forgot their prefix

@bot.listen()
async def on_message(msg):

  if msg.content == "<@!810662403217948672> prefix":
    await msg.channel.send(f'The prefix of this bot on this server is `{db[str(msg.guild.id)]}`')

  



    
  


    




@bot.command()
async def stop_drops(ctx):

  if int(ctx.author.id) != 751594192739893298:
    embed = discord.Embed(title='Hey!', description=":x: You don't have permission to use this command!")
    await ctx.send(embed=embed)
    return

  else:
    task.cancel()
    await ctx.channel.send('refugee drops have stopped')

@bot.command()
async def start_drops(ctx):
  if int(ctx.author.id) != 751594192739893298:
    return

  else:
    try:
      global task
      task = bot.loop.create_task(refugee_drops())
      await ctx.channel.send('refugee drops have started')
    except:
      await ctx.channel.send('Drops are have already started')

#a verrryyy fun game
@bot.command()
async def guess_capital(ctx, *arg):
  the_author = ctx.message.author
  channel = ctx.message.channel

  await ctx.channel.send("How long should the time limit be (**in seconds**)")

  def check1(m):
    return m.content.isdigit() and m.author == the_author and m.channel == channel and int(m.content) <= 300

  msg1 = await bot.wait_for("message", check=check1)

  length = int(msg1.content)

  
  correct_ans = {}

  

  if len(arg) == 0 or len(arg) >= 1 and arg[0].lower() != 'reverse':
    count = 0
    bol = True
    while bol:
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
        return fuzz.ratio(country_capital.lower(), m.content.lower()) > 85 or m.content.lower() == 'quit' and m.channel == channel

      try:
        msg = await bot.wait_for('message', check=check, timeout=length)

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
        msg = await bot.wait_for('message', check=check, timeout=length)

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
  

@bot.command(name='calc')
async def my_command(ctx, *, arg):
    result = eval(arg)
    await ctx.send(result)

#a command to give the capital of a country
@bot.command(name='capital')
async def cap(ctx, *, country):

    try:
    
      if fuzz.ratio(country, "England") > 80:
        country1 = CountryInfo('Great Britan')
      else:
        country1 = CountryInfo(country)

      result = country1.capital()

    

      embed = discord.Embed(
              title="Capital of " + country,
              description="**The capital of {country} is `{result}`**".format(
                  result=result, country=country),
              color=0xFF5733)

      result4 = coco.convert(names=country, to='ISO2')
      embed.set_thumbnail(
              url=f'https://flagcdn.com/w80/{result4.lower()}.jpg')

      embed.set_footer(
              text="Requested by: {name}".format(name=ctx.message.author),
              icon_url=ctx.author.avatar_url)

      await ctx.channel.send(embed=embed)

    except:
        embed = discord.Embed(
           title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@cap.error
async def capital_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}capital <country>```')
    await ctx.channel.send(embed=embed)


@war.error
async def work_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}war <user>``` User should be a ping')
    await ctx.channel.send(embed=embed)
  



  
  



#a command to give the population of a country
@bot.command()
async def population(ctx, *, country):

    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.population()

        result1 = "{:,}".format(result)

        embed = discord.Embed(
            title="Population of " + country,
            description='**`{result1}`**'.format(result1=result1),
            color=0xFF5733)

        result4 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result4.lower()}.jpg')

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.message.author),
            icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@population.error
async def population_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}population <country>```')
    await ctx.channel.send(embed=embed)

#a command to give the area of a country, in sq. km
@bot.command()
async def area(ctx, *, country):
    try:
        country1 = CountryInfo(country)
        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")
        result = country1.area()

        result1 = "{:,}".format(result)
        result1 = str(result1)
        

        embed = discord.Embed(
            title="Area of " + country,
            description=f'**`{result1}` sq. km**',
            color=0xFF5733)

        result4 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result4.lower()}.jpg')

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.message.author),
            icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(
            title="Sorry",
            description=" **{country} is not a country**".format(
                country=country),
            color=0xFF5733)
        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@area.error
async def area_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}area <country>```')
    await ctx.channel.send(embed=embed)



@bot.command()
async def states(ctx, *, country):
    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.provinces()

        for i in range(0, len(result)):
          result[i] = '`' +result[i]+ '`'

        result1 = " |".join(result)

        result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

        embed = discord.Embed(
            title="States of " + country,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        result4 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result4.lower()}.jpg')

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.message.author),
            icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)


@states.error
async def states_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}states <country>```')
    await ctx.channel.send(embed=embed)

@bot.command()
async def language(ctx, *, country):
    try:
        country1 = CountryInfo(country)
        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.languages()

        for i in range(0, len(result)):
            result3 = pycountry.languages.get(alpha_2=result[i])

            result[i] = result3.name

        result1 = " |".join(result)

        result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

        result4 = coco.convert(names=country, to='iso2')

        if country == 'malaysia' or country == 'Malaysia':

            embed = discord.Embed(title="Language(s) of " + country,
                                  description='**Malay**',
                                  color=0xFF5733)

            result4 = coco.convert(names=country, to='ISO2')
            embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result4.lower()}.jpg')

            embed.set_footer(
                text="Requested by: {name}".format(name=ctx.message.author),
                icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Language(s) of " + country,
                description='**`{result2}`**'.format(result2=result2),
                color=0xFF5733)

            result4 = coco.convert(names=country, to='ISO2')
            embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result4.lower()}.jpg')

            embed.set_footer(
                text="Requested by: {name}".format(name=ctx.message.author),
                icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)

    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)


@language.error
async def language_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}language <country>```')
    await ctx.channel.send(embed=embed)

@bot.command()
async def region(ctx, *, country):

    try:
        country1 = CountryInfo(country)
        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.region()

        embed = discord.Embed(title="Region for " + country,
                              description='**`{result}`**'.format(result=result),
                              color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.message.author),
            icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)
        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@region.error
async def region_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}region <country>```')
    await ctx.channel.send(embed=embed)

@bot.command()
async def subregion(ctx, *, country):

    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.subregion()

        embed = discord.Embed(title="Subregion for " + country,
                              description='**`{result}`**'.format(result=result),
                              color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.message.author),
            icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@subregion.error
async def subregion_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}subregion <country>```')
    await ctx.channel.send(embed=embed)

@bot.command()
async def start(ctx):
  try:
    embed = discord.Embed(title="Hooray", description='''We are very excited for you to start your own country :tada:
    In the chat type the **name** of your soon to be country''', color=Color.teal())

    await ctx.channel.send(embed=embed)
    the_channel, the_author = ctx.channel, ctx.message.author

    def check(m):
      return m.channel == the_channel and m.author == the_author

    msg = await bot.wait_for('message', check=check, timeout=100)

    writing((ctx.author.id, msg.content, 0, 1, "Mayor", 1, 0, 1000000000, 0, 0, 0, 0))

    await ctx.channel.send('Hooray, Country Created!!!!')
  except:
    embed = discord.Embed(title='Sorry', description=''':x: You already have a country.''')

    await ctx.channel.send(embed=embed)


@bot.command()
async def profile(ctx, *arg):
  if len(arg) == 0:
    try:
      a = reading(ctx.message.author.id)
      name = a[0][0]
      
      embed = discord.Embed(title=f'''{name}''', description=f'''Population: `{"{:,}".format(a[0][1])}`
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

      embed.set_thumbnail(url=ctx.author.avatar_url)
      if dic[a[0][4]] == "Mom's basement":
        embed.set_image(url='http://www.storefrontlife.com/wp-content/uploads/2013/01/Basement.jpg')
      elif dic[a[0][4]] == 'Apartment (with roomate)': 
        embed.set_image(url='https://res.cloudinary.com/hemcfvrk2/image/upload/c_lfill,g_xy_center,x_1516,y_615,w_1200,h_700,q_auto:eco,fl_lossy,f_auto/v1485383879/uhzs2wektoh0mb5rkual.jpg')
      
      elif dic[a[0][4]] == 'Mansion':
        embed.set_image(url='https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2013/08/26/100987825-121017_EJ_stone_mansion_0014r.600x400.jpg?v=1395082652')

      
      elif dic[a[0][4]] == 'Home Office':
        embed.set_image(url='https://blog-www.pods.com/wp-content/uploads/2020/07/Feature-Home-Office-GEtty-Resized.jpg')

      elif dic[a[0][4]] == 'Space Base':
        embed.set_image(url='https://cdna.artstation.com/p/assets/images/images/000/630/350/large/jarek-kalwa-space-base.jpg?1429173581')

      embed.set_footer(text=f'Tax your citizens with `{db[str(ctx.guild.id)]}tax` to earn coins!')
      
      await ctx.channel.send(embed=embed)

    except:
      embed= discord.Embed(title='Sorry', description=f''':x: You don't have a country yet. Type {db[str(ctx.guild.id)]}start to create your amazing country!!!''')

      await ctx.channel.send(embed=embed)
  else:
    b = arg[0]
    b = b.replace("<","")
    b = b.replace(">","")
    b = b.replace("@","")
    b = b.replace("!", "")
    
    try:
      a = reading(b)

      name = a[0][0]


      embed = discord.Embed(title=f'''{name}''', description=f'''Population: `{a[0][1]}`
                      Multiplier: `{a[0][2]}`
                      Job: `{a[0][3]}`
                      Work Ethic: `{a[0][4]}`
                      Office: `{dic[a[0][4]]}`
                      Work Commands Issued: 
                      `{a[0][10]}`
                      Coins: {a[0][11]} :coin:
                      ''')
      
      username = await bot.fetch_user(b)
      
      embed.add_field(name='War', value=f'''Wars Played: `{a[0][7]}`
                      Wars Won: `{a[0][8]}`
                      Wars Lost: `{a[0][9]}`
                      ''')

      embed.add_field(name='Prestige', value=f'''Prestige Level: `{a[0][5]}`
                      Prestige Requirement `{a[0][6]}` population''')
      

      
      if dic[a[0][4]] == "Mom's basement":
        embed.set_image(url='http://www.storefrontlife.com/wp-content/uploads/2013/01/Basement.jpg')

      elif dic[a[0][4]] == 'Apartment (with roomate)':
        embed.set_image(url='https://res.cloudinary.com/hemcfvrk2/image/upload/c_lfill,g_xy_center,x_1516,y_615,w_1200,h_700,q_auto:eco,fl_lossy,f_auto/v1485383879/uhzs2wektoh0mb5rkual.jpg')
      elif dic[a[0][4]] == 'Home Office':
        embed.set_image(url='https://blog-www.pods.com/wp-content/uploads/2020/07/Feature-Home-Office-GEtty-Resized.jpg')

      elif dic[a[0][4]] == 'Mansion':
        embed.set_image(url='https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2013/08/26/100987825-121017_EJ_stone_mansion_0014r.600x400.jpg?v=1395082652')
      elif dic[a[0][4]] == 'Space Base':
        embed.set_image(url='https://cdna.artstation.com/p/assets/images/images/000/630/350/large/jarek-kalwa-space-base.jpg?1429173581')

      embed.set_thumbnail(url=username.avatar_url)
      await ctx.channel.send(embed=embed)
    except:
      embed = discord.Embed(title='Sorry', description=":x: This user doesn't have a country")

      await ctx.channel.send(embed=embed)

@bot.command(aliases=['shop'])
async def store(ctx):
  try: 
     a = reading(ctx.message.author.id)
  except:
    embed = discord.Embed(title='Whoops', description=f"You haven't started a country yet. Type `{db[ctx.guild.id]}start` to create your amazing country!!!!")
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
  To buy this item type: `{db[str(ctx.guild.id)]}buy 1 <amount>`
  Cost: 10,000 people in your country will leave
  Increases your multiplier by 1
  
  **2. Apartment (with roomate) ID = `2` Status: [{status}]**
  To buy this item type: `{db[str(ctx.guild.id)]}buy 2`

  Cost:  1000 people think you spend too much and they leave.
  
  Your work ethic becomes 2 
  
  
  3. **Home Office :homes:  ID = `3` Status: [{status2}]**
  To buy this item type: `{db[str(ctx.guild.id)]}buy 3`

  Cost: 10,000 people think you spend too much and they leave.
  
  Your work ethic becomes 3 
  
  
  4. **Mansion :homes:  ID = `4` Status: [{status3}]**
  To buy this item type: `{db[str(ctx.guild.id)]}buy 4`

  Cost: 50,000 people think you spend too much and they leave.
  
  Your work ethic becomes 5 
  
  5. **Space Base :crescent_moon:  ID = 5 Status: [{status4}]**
  To buy this item type: `{db[str(ctx.guild.id)]}buy 5`

  Cost: 100,000 people think you spend too much and they leave.
  
  Your work ethic becomes 10 ''')

  await ctx.channel.send(embed=embed)



@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def work(ctx):
  chance = random.randint(1, 10)
  try:
    a = reading(ctx.message.author.id)
  except:
    embed = discord.Embed(title='Sorry', description=f":x: You haven't created a country yet. To create one type `{db[str(ctx.guild.id)]}start`. Have fun with your amazing country!!!")
    await ctx.channel.send(embed=embed)
    return

  if a[0][1] > 30000000000000000000000000000000000:
    embed = discord.Embed(title='Woah!', description='You have the max amount of populatio even possible! You better prestige!')
    await ctx.channel.send(embed=embed)
    return
  if a[0][1] >= 100 and a[0][3] == 'Mayor':
    embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `State Senator`')
    await ctx.channel.send(embed=embed)
    update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'State Senator', a[0][4], a[0][10]))
    a = reading(ctx.message.author.id)

  elif a[0][1] >= 10000 and a[0][3] == 'State Senator':
    embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `Governor`')
    await ctx.channel.send(embed=embed)
    update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'Governor', a[0][4], a[0][10]))
    a = reading(ctx.message.author.id)

  elif a[0][1] >= 50000 and a[0][3] == 'Governor':
    embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `Senator`')
    await ctx.channel.send(embed=embed)
    update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'Senator', a[0][4], a[0][10]))
    a = reading(ctx.message.author.id)

  elif a[0][1] >= 200000 and a[0][3] == 'Senator':
    embed = discord.Embed(title='Promotion!!!!', description='Congratulations!!, You have been promoted to `Vice President`')

    await ctx.channel.send(embed=embed)
    update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'Vice President', a[0][4], a[0][10]))
    a = reading(ctx.message.author.id)

  elif a[0][1] >= 2500000 and a[0][3] == 'Vice President':
    embed = discord.Embed(title='Promotion!!!!', description=f'Congratulations!!, You have been promoted to `President` You are now the leader of {a[0][0]}')
    await ctx.channel.send(embed=embed)
    update((ctx.message.author.id, a[0][0], a[0][1],a[0][2],'President', a[0][4], a[0][10]))
    a = reading(ctx.message.author.id)


  
 
  
  
  
  if a[0][3] == 'Mayor':
    amount1 = random.randint(0, 5)
    amount1 = amount1 * a[0][4]
    if float(a[0][2]).is_integer():
      embed=discord.Embed(title='Boost Time!!!!! :zap:', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
      await ctx.channel.send(embed=embed)
      amount1 = amount1 * a[0][2]


    amount = amount1 + int(a[0][1])
    multi = float("{:.1f}".format(a[0][2] + (a[0][5] +1)/10))
    update((ctx.message.author.id, a[0][0], amount,multi, 'Mayor', a[0][4], a[0][10] + 1))

    

    embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

    await ctx.channel.send(embed=embed)
    if chance == 5:
      a = reading(ctx.message.author.id)
      update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
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
    update((ctx.message.author.id, a[0][0], amount,multi, 'State Senator', a[0][4], a[0][10] + 1))

    embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

    await ctx.channel.send(embed=embed)
    if chance ==  5:
      a = reading(ctx.message.author.id)
      update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
      embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
      await ctx.channel.send(embed=embed_chance)
  
  elif a[0][3] == 'Governor':
    amount1 = random.randint(100, 1000)
    amount1 = amount1 * a[0][4]
    if float(a[0][2]).is_integer():
      embed=discord.Embed(title='Boost Time!!!!! :zap:', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
      await ctx.channel.send(embed=embed)
      amount1 = amount1 * a[0][2]

    

    amount = amount1 + int(a[0][1])
    multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
    update((ctx.message.author.id, a[0][0], amount,multi, 'Governor', a[0][4], a[0][10] + 1))

    embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

    await ctx.channel.send(embed=embed)
    if chance == 5:
      a = reading(ctx.message.author.id)
      update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
      embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
      await ctx.channel.send(embed=embed_chance)
  
  elif a[0][3] == 'Senator':
    amount1 = random.randint(1000, 10000)
    amount1 = amount1 * a[0][4]
 
    if float(a[0][2]).is_integer():
      embed=discord.Embed(title='Boost Time :zap:!!!!!', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
      await ctx.channel.send(embed=embed)
      amount1 = amount1 * a[0][2]
    amount = amount1 + int(a[0][1])
    multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
    update((ctx.message.author.id, a[0][0], amount,multi, 'Senator', a[0][4], a[0][10] + 1))

    embed = discord.Embed(title='Work Work Work :zap:!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

    await ctx.channel.send(embed=embed)
    if chance == 5:
      a = reading(ctx.message.author.id)
      update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
      embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
      await ctx.channel.send(embed=embed_chance)
  
  elif a[0][3] == 'Vice President':
    amount1 = random.randint(10000, 100000)
    amount1 = amount1 * a[0][4]
    if float(a[0][2]).is_integer():
      embed=discord.Embed(title='Boost Time :zap:!!!!!', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
      await ctx.channel.send(embed=embed)
      amount1 = amount1 * a[0][2]


    amount = amount1 + int(a[0][1])
    multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
    update((ctx.message.author.id, a[0][0], amount,multi, 'Vice President', a[0][4], a[0][10] + 1))

    embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

    await ctx.channel.send(embed=embed)
    if chance == 5:
      a = reading(ctx.message.author.id)
      update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
      embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
      await ctx.channel.send(embed=embed_chance)

  elif a[0][3] == 'President':
    amount1 = random.randint(100000, 1000000)
    amount1 = amount1 * a[0][4]
    if float(a[0][2]).is_integer():
      embed=discord.Embed(title='Boost Time!!!!! :zap:', description=f'''Your work will be multiplied by `{str(a[0][2])}`''')
      await ctx.channel.send(embed=embed)
      amount1 = amount1 * a[0][2]
    amount = amount1 + int(a[0][1])
    multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1)/10)))
    update((ctx.message.author.id, a[0][0], amount,multi, 'President', a[0][4], a[0][10] + 1))

    embed = discord.Embed(title='Work Work Work!!!!!', description=f'''During your work shift, you got `{amount1}` more people into your country!!''')

    await ctx.channel.send(embed=embed)
    if chance == 5:
      a = reading(ctx.message.author.id)
      update((ctx.message.author.id, a[0][0], a[0][1], a[0][2] + 1, a[0][3], a[0][4], a[0][10]))
      embed_chance = discord.Embed(title='Hooray', description='While working you found 1 multiplier boost :zap:')
      await ctx.channel.send(embed=embed_chance)
  

@work.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="Too tired",description=f'''You are too tired to work again. You can work in `{error.retry_after:.2f}`s.''')
        await ctx.send(embed=em)


@bot.command()
async def prestige(ctx):
  try:
    a = reading(ctx.message.author.id)
  except:
    embed = discord.Embed(title='Sorry', description=f":x: You haven't created a country yet. To create one type `{db[str(ctx.guild.id)]}start`. Have fun with your amazing country!!!")
    await ctx.channel.send(embed=embed)
    return
  

  
  if a[0][1] > a[0][6]:
    embed = discord.Embed(title='Hooray!!', description='You have met the requirements to prestige!! Do you want to prestige `y` | `n`')
    await ctx.channel.send(embed=embed)
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.message.author

    msg = await bot.wait_for('message', check=check, timeout=100)

    if msg.content == 'n':
      embed = discord.Embed(title='Ok', description=':x: Prestige cancelled')
      await ctx.channel.send(embed=embed)

    elif msg.content == 'y':
      update_prestige((ctx.message.author.id, a[0][0], 0, 1, 'Mayor', 1, a[0][5] + 1, (a[0][6] + 1000000000)))
      embed = discord.Embed(title='Congratulations', description=':tada: You prestiged!!')
      await ctx.channel.send(embed=embed)
      update_coins(ctx.author.id, 0)
  else:
    embed = discord.Embed(title='Oh No', description=''':x: you haven't met the requirements to prestige''')
    await ctx.channel.send(embed=embed)
    
@bot.command()
async def quit(ctx):
  embed = discord.Embed(title='quit', description=':x: Are you really sure you want to quit your country. You will lose all your data (`y`,`n`)')
  await ctx.channel.send(embed=embed)
  thechannel = ctx.channel
  theauthor = ctx.message.author
  def check(m):
    return m.content == 'y' or m.content == 'n' and m.channel == thechannel and m.author == theauthor 
  msg = await bot.wait_for('message', check=check, timeout=100)
  try:
    a = reading(ctx.message.author.id)
    if msg.content == 'y':
      delete_task(ctx.message.author.id)
      embed = discord.Embed(title="Country deleted", description=f"Your country is gone, and you can't become the leader :cry:. But don't worry :D. You can start a new one with `{db[str(ctx.guild.id)]}start`")
      await ctx.channel.send(embed=embed)
    elif msg.content == 'n':
      embed = discord.Embed(title='Phew', description=f'Your country is not deleted :DD')
      await ctx.channel.send(embed=embed)
  except:
    embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{db[str(ctx.guild.id)]}start`''')
    await ctx.channel.send(embed=embed)


@bot.command()
async def buy(ctx, *id):

  try:
    a = reading(ctx.message.author.id)
  except:
    embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{db[str(ctx.guild.id)]}start`''')
    await ctx.channel.send(embed=embed)
  if len(id) == 0:
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}buy <ID> <amount>```')
    await ctx.channel.send(embed=embed)
    return


  if len(id) == 2:
    amount = id[1]
    if id[0] == '1':
        if a[0][1] - (10000 * int(amount)) < 0:
          embed = discord.Embed(title='Oh no', description=''':x: You don't have a big enough population''')
          await ctx.channel.send(embed=embed)
          return

        if a[0][2] > 10000000:
          embed = discord.Embed(title='Stop!', description="You can't buy anymore multiplier!!")
          await ctx.channel.send(embed=embed)
          return

        update((ctx.message.author.id, a[0][0], a[0][1] - (10000 * int(amount)), a[0][2] + (1 * int(amount)), a[0][3], a[0][4], a[0][10]))

        embed = discord.Embed(title='Congratulations',
          description=f'You have bought {amount} Multiplier Boosts')
        await ctx.channel.send(embed=embed)

      

      

  elif len(id) == 1:
    if id[0] == '1':
      embed = discord.Embed(title='Error', description=':x: How much multiplier are you buying!')
      await ctx.channel.send(embed=embed)

    if id[0] == '2':
      if a[0][4] >= 2:
        embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
        await ctx.channel.send(embed=embed)
        return
      if (a[0][1] - 1000) < 0:
        embed = discord.Embed(title='Oh no', description=''':x: You don't have a big enough population''')
        await ctx.channel.send(embed=embed)
        return

      
      update((ctx.message.author.id, a[0][0], a[0][1] - (1000), a[0][2], a[0][3], (a[0][4] + 1), a[0][10]))

      embed = discord.Embed(title='Congratulations',
        description=f'You have bought the Apartment (with roomate)')
      await ctx.channel.send(embed=embed)

    if id[0] == '3':
      if a[0][4] >= 3:
        embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
        await ctx.channel.send(embed=embed)
        return
      elif a[0][4] < 2:
        embed = discord.Embed(title='Hey', description=':x: You need to buy the apartment first!!!')
        await ctx.channel.send(embed=embed)
        return
      if (a[0][1] - 10000) < 0:
        embed = discord.Embed(title='Oh no', description=''':x: You don't have a big enough population''')
        await ctx.channel.send(embed=embed)
        return

      
      update((ctx.message.author.id, a[0][0], a[0][1] - (10000), a[0][2], a[0][3], (a[0][4] + 1), a[0][10]))

      embed = discord.Embed(title='Congratulations',
        description=f'You have bought the Home Office')
      await ctx.channel.send(embed=embed)

    if id[0] == '4':
      if a[0][4] >= 5:
        embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
        await ctx.channel.send(embed=embed)
        return
      if a[0][4] < 3:
        embed = discord.Embed(title='Hey', description=':x: You need to buy the Home Office first!!!')
        await ctx.channel.send(embed=embed)
        return
      if (a[0][1] - 50000) < 0:
        embed = discord.Embed(title='Oh no', description=''':x: You don't have a big enough population''')
        await ctx.channel.send(embed=embed)
        return

      
      update((ctx.message.author.id, a[0][0], a[0][1] - (50000), a[0][2], a[0][3], (a[0][4] + 2), a[0][10]))

      embed = discord.Embed(title='Congratulations',
        description=f'You have bought the Mansion')
      await ctx.channel.send(embed=embed)
    
    if id[0] == '5':
      if a[0][4] >= 10:
        embed = discord.Embed(title='Hey', description=':x: You already own this!!!')
        await ctx.channel.send(embed=embed)
        return
      if a[0][4] < 5:
        embed = discord.Embed(title='Hey', description=':x: You need to buy the Mansion first!!!')
        await ctx.channel.send(embed=embed)
        return
      if (a[0][1] - 100000) < 0:
        embed = discord.Embed(title='Oh no', description=''':x: You don't have a big enough population''')
        await ctx.channel.send(embed=embed)
        return

      
      update((ctx.message.author.id, a[0][0], a[0][1] - (100000), a[0][2], a[0][3], (a[0][4] + 5), a[0][10]))

      embed = discord.Embed(title='Congratulations',
        description=f'You have bought the Space Base')
      await ctx.channel.send(embed=embed)
      

@bot.command()
async def gift(ctx, user1, amount):
  try:
    b = user1.replace("<","")
    b = b.replace(">","")
    b = b.replace("@","")
    user = b.replace("!", "")

    

    a = reading(user)

  except:
    embed = discord.Embed(title='Whoops', description=':x: This person doesnt have a country!!')
    await ctx.channel.send(embed=embed)
    return

 

  if str(user) == str(ctx.message.author.id):
      embed=discord.Embed(title='Hey!', description=":x: You can't give gifts to yourself!")
      await ctx.channel.send(embed=embed)
      return

  try:
    b = reading(ctx.author.id)

  except:
    embed = discord.Embed(title='Whoops', description=f":x: You don't have a country!! Type `{db(str(ctx.guild.id))}start` to start your country!")
    await ctx.channel.send(embed=embed)
    return

  amount = amount.strip(',')
  if amount.isnumeric():
    if int(amount) > b[0][1]:
      embed = discord.Embed(title="Hey!", description=":x: You don't have that many people!")
      await ctx.channel.send(embed=embed)
      return

    else:
        update((ctx.author.id, b[0][0], b[0][1] - int(amount), b[0][2], b[0][3], b[0][4], b[0][10]))

        update((user, a[0][0], a[0][1] + int(amount), a[0][2], a[0][3], a[0][4], a[0][10]))

        await ctx.channel.send(embed=discord.Embed(title="Success!", description=f"Succesfully transefered {amount} people to {user1}'s country!"))
    
  else:
    
    if amount.lower() == 'half':
        update((ctx.author.id, b[0][0], int(b[0][1]/2), b[0][2], b[0][3], b[0][4], b[0][10]))

        update((user, a[0][0], a[0][1] + int(b[0][1]/2), a[0][2], a[0][3], a[0][4], a[0][10]))

        await ctx.channel.send(embed=discord.Embed(title="Success!", description=f"Succesfully transefered {int(b[0][1]/2)} people to {user1}'s country!"))

        return

    elif amount.lower() == 'all':
        update((ctx.author.id, b[0][0], 0, b[0][2], b[0][3], b[0][4], b[0][10]))

        update((user, a[0][0], a[0][1] + b[0][1], a[0][2], a[0][3], a[0][4], a[0][10]))

        await ctx.channel.send(embed=discord.Embed(title="Success!", description=f"Succesfully transefered {int(b[0][1])} people to {user1}'s country!"))

        return
    embed = discord.Embed(title='Hey!', description=":x: That is not a valid amount!")
    await ctx.channel.send(embed=embed)

    
    
  

  

@bot.command()
async def change(ctx, *, arg):
  try:
    a = reading(ctx.message.author.id)
  except:
    embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{db[str(ctx.guild.id)]}start`''')
    await ctx.channel.send(embed=embed)

  if len(arg) > 50:
    embed = discord.Embed(title='Hey!', description=':x: The name can only be up to 50 characters')
    await ctx.channel.send(embed=embed)
    return

  arg = arg.replace("'", "`")
  update((ctx.message.author.id, arg, a[0][1], a[0][2], a[0][3], a[0][4], a[0][10]))
  embed = discord.Embed(title='Success', description=f'Country name Has been succesfully changed to {arg}')

  await ctx.channel.send(embed=embed)

@change.error
async def change_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}change <new country name>```')
    await ctx.channel.send(embed=embed)

@commands.cooldown(1, 86400, commands.BucketType.user)
@bot.command()
async def daily(ctx):
  a = reading(ctx.message.author.id)
  update((ctx.message.author.id, a[0][0], a[0][1] + 100, a[0][2], a[0][3], a[0][4], a[0][10]))

  b = reading(ctx.message.author.id)

  embed = discord.Embed(title='Daily', description=f'`100` more people joined your country!! Your new population is `{b[0][1]}`')

  await ctx.channel.send(embed=embed)

@daily.error
async def daily_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
          time1 = error.retry_after
          em = discord.Embed(title="Slow it down!",description=f'''Try again after `{datetime.timedelta(seconds = time1)}`.''')
          await ctx.send(embed=em)



    


@gift.error
async def gift_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
      embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}gift <user> <amount>```')
      await ctx.channel.send(embed=embed)




@bot.command()
async def timezone(ctx, *, country):
    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.timezones()

        for i in range(0, len(result)):
          result[i] = '`' +result[i]+ '`'

        result1 = " |".join(result)

        result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

        embed = discord.Embed(
            title="Timezone(s) of " + country,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

        embed.set_footer(
            text="Requested by: {name}".format(name=ctx.message.author),
            icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@timezone.error
async def timezone_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}timezone <country>```')
    await ctx.channel.send(embed=embed)


@bot.command()
async def borders(ctx, *, country):
    try:
        country1 = CountryInfo(country)
 
        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.borders()

        result1 = cc.convert(names=result, to='name_short', not_found=False)

       

        if isinstance(result1, str) == True:
            embed = discord.Embed(
                title="Borders of " + country,
                description=f'**`{result1}`**',
                color=0xFF5733)

            result5 = coco.convert(names=country, to='ISO2')
            embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result5.lower()}.jpg')

            embed.set_footer(text="Requested by: {name}".format(
                name=ctx.message.author),
                              icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)

        elif type(result1) == type([]):
            for i in range(0, len(result1)):
              result1[i] = '`' +result1[i]+ '`'

            result1 = " ".join(result1)


            if not result1:
                embed = discord.Embed(
                    title="Borders of " + country,
                    description=
                    '**There are no countries {country} borders :(**'.format(
                        country=country),
                    color=0xFF5733)

                result5 = coco.convert(names=country, to='ISO2')
                embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result5.lower()}.jpg')

                embed.set_footer(text="Requested by: {name}".format(
                    name=ctx.message.author),
                                 icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Borders of " + country,
                    description=f'**{result1}**',
                    color=0xFF5733)

                result5 = coco.convert(names=country, to='ISO2')
                embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result5.lower()}.jpg')

                embed.set_footer(text="Requested by: {name}".format(
                    name=ctx.message.author),
                                 icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)

    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@borders.error
async def borders_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}borders <country>```')
    await ctx.channel.send(embed=embed)


@bot.command()
async def coords(ctx, *, country):
    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.latlng()

        for i in range(0, len(result)):
            result[i] = str(result[i])

        result1 = ",".join(result)

        result2 = re.sub(r'(?<=[,])(?=[^\s])', r' ', result1)

        embed = discord.Embed(
            title="Coordinates of " + country,
            description='**`{country}` is located at the coordinates: `{result2}`**'
            .format(result2=result2, country=country),
            color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

        embed.set_footer(text="Information requested by: {}".format(
            ctx.author.display_name))

        await ctx.channel.send(embed=embed)

    except:
        embed = discord.Embed(
            title="Sorry",
            description="**{country} is not a country**".format(
                country=country),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)


@coords.error
async def coords_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}coords <country>```')
    await ctx.channel.send(embed=embed)





  
  







@bot.command()
async def covid(ctx, *, arg):
  try:
    url="https://covid-193.p.rapidapi.com/statistics?country={}".format(arg)

    

    headers = {
      'x-rapidapi-key': "f3c7547811mshb7e5680d6a29edcp1387fcjsncb14f156c54a",
      'x-rapidapi-host': "covid-193.p.rapidapi.com"
      }

    response = requests.request("GET", url, headers=headers)
    new_dict = json.loads(response.text)

    dict1 = new_dict['response']

    dict2 = dict1[0]
    dict3 = dict2['cases']
    new_cases = dict3['new']
    active_cases = dict3['active']
    critical_cases = dict3['critical']
    recovered = dict3['recovered']
    cases_per1mill = dict3['1M_pop']
    total_cases = dict3['total']

    deaths = dict2["deaths"]

  

    deaths_per1mill = deaths["1M_pop"]

    new_deaths = deaths['new']

    total_deaths = deaths['total']

    day = dict2['day']

  

    



    if not new_cases:
      pass
    else:
      new_cases = new_cases[1:]
      new_cases = "{:,}".format(int(new_cases))
    if not active_cases:
      pass
    else:
      active_cases = "{:,}".format(int(active_cases))

    if not critical_cases:
      pass
    else:
      critical_cases = "{:,}".format(int(critical_cases))
    
    if not recovered:
      pass
    else:
      recovered = "{:,}".format(int(recovered))

    
    if not cases_per1mill:
      pass
    else:
      cases_per1mill = "{:,}".format(int(cases_per1mill))

    if not total_cases:
      pass
    else:
      total_cases = "{:,}".format(int(total_cases))

    if not deaths_per1mill: pass
    else: deaths_per1mill = "{:,}".format(int(deaths_per1mill))

    if not new_deaths: pass
    else: new_deaths = "{:,}".format(int(new_deaths))

    if not total_deaths: pass
    else: total_deaths = "{:,}".format(int(total_deaths))
      
    
    
    embed = discord.Embed(
              title="Covid 19 info for " + arg,
              description=None,color=Color.from_rgb(0, 0, 0))

    embed.add_field(name="Cases", value = f'''New cases: `{new_cases}`
                              Active cases: `{active_cases}`
                              Critical cases: `{critical_cases}`
                              Recovered: `{recovered}`
                              Cases per 1 million people: `{cases_per1mill}`
                              Total cases: `{total_cases}`''', inline=True)

    embed.add_field(name="Deaths", value = f'''New deaths: `{new_deaths}`
    Deaths per 1 million people: `{deaths_per1mill}`
    Total deaths: `{total_deaths}`''', inline=True)

    
    embed.set_thumbnail(
              url='https://cdn.discordapp.com/attachments/239446877953720321/691020838379716698/unknown.png')

    embed.set_footer(text=f"Date: {datetime.datetime.now()}")

    await ctx.channel.send(embed=embed)
  
  except:
    embed = discord.Embed(title="Sorry",description="**We could not find data for {}**".format(arg), color=0xFF5733)

    embed.set_thumbnail(
           url=
          'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

    await ctx.channel.send(embed=embed)

@covid.error
async def covid_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}covid <country>```')
    await ctx.channel.send(embed=embed)

#city_weather command





@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
      main_message = ctx.message.content.split(' ')[0]
      
      similar = []
      other=[]
      
     
      for commands in bot.commands:
        
        if fuzz.ratio(main_message, commands.name) > 50:
          similar.append(f'`{db[ctx.guild.id]}{commands.name}`')
          other.append(commands)
      
      
      if len(similar) == 0:
        return
      similar = ' '.join(similar)

      
     
      
      if similar == '`.work`':
        await ctx.channel.send(f"Did you mean {similar}")
        return

      elif similar == '`.tax`':
        await ctx.channel.send(f"Did you mean {similar}")
        return
      elif similar == '`.daily`':
        await ctx.channel.send(f"Did you mean {similar}")
        return
      try:
        await ctx.invoke(other[0])

      except:
        await ctx.channel.send(f"Did you mean {similar}")

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
       pass

    else:
       raise error


@bot.command()
async def aww(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/awww').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)


@bot.command()
async def snake(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/snakes').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)


@bot.command()
async def cat(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/cats').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)



@bot.command()
async def dog(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/dog').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)




    


    

@bot.command()
async def meme(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/wholesomememes').json()
  meme = data
  channel_nsfw = ctx.message.channel.is_nsfw()
  title = meme['title']
  
  if meme['nsfw'] == 'True':
    if channel_nsfw:
      embed = discord.Embed(title=f'{title} [NSFW]', url=meme['postLink'])
      embed.set_image(url=meme['url'])
      author = meme['author']
      likes = meme['ups']
      embed.set_footer(text=f'Author: {author} | 👍 {likes}')
      await ctx.send(embed=embed)

    else:
      embed = discord.Embed(title='Hey!', description=':x: This meme is NSFW!!! You can only see it in an NSFW channel.')
      await ctx.send(embed=embed)

    

  else:
    embed = discord.Embed(title=meme['title'], url=meme['postLink'])
    embed.set_image(url=meme['url'])
    author = meme['author']
    likes = meme['ups']
    embed.set_footer(text=f'Author: {author} | 👍 {likes}')
    await ctx.send(embed=embed)
    


@bot.command()
async def help(ctx, *arg):
    prefix = db[str(ctx.guild.id)]
    if len(arg) == 0:
        main = discord.Embed(title="Country Bot Help",
                              description=f'''**Prefix = `{prefix}`
      
          Type `{prefix}help <command>` for more information on a specific  command. (HIGHLY RECOMMENDED)
          
          Forgot the bot's prefix?
          Don't worry type **<@!810662403217948672> prefix** and Country Bot will tell you its prefix for this server**

          **Links: [vote (top.gg)](https://top.gg/bot/810662403217948672/vote) | [invite](https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands) | [top.gg](https://top.gg/bot/810662403217948672#/) | [support server](https://discord.gg/hCgh9wngkS) | [discordbotlist](https://discord.ly/country-bot)**
          
          Tip: Use `{db[ctx.guild.id]}war @Player` to wage war on your friends countries!!

          Tip2: Use `{db[ctx.guild.id]}daily` to receive 100 population every day!

          **Check out `.changelog` to see new features that have come out!!!**



      ''', color=0xFF5733)

        main.set_thumbnail(
            url= main_url
            
        )

        message = await ctx.channel.send(embed=main)
                            

          

        contents = [main, geographical, economy, general, country_database, admin_stuff, games, misc, gambling, developer_commands]

        pages = len(contents)
        cur_page = 1

        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        await message.add_reaction("❌")

        def check2(reaction, user):
          return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "⏩", "⏪", "❌"] and reaction.message == message

        



        
        while True:
          try:
            reaction, user = await bot.wait_for("reaction_add", timeout=100, check=check2)

            

          
            
            if str(reaction.emoji) == "▶️" and cur_page < pages:
                cur_page += 1
                
                await message.edit(embed=contents[cur_page-1])
                

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                
                await message.edit(embed=contents[cur_page-1])
                

            elif str(reaction.emoji) == "⏩":
              cur_page = pages
              
              await message.edit(embed=contents[cur_page-1])
              
            
            elif str(reaction.emoji) == "⏪":
              cur_page = 1
              await message.edit(embed=contents[0])
              
            
            elif str(reaction.emoji) == "❌":
              await message.delete()
              break
            
          except asyncio.TimeoutError:
            await message.delete()
            break

        
      

        

        

      

        

        


        

        
    if len(arg) == 1:
        arg = ' '.join(arg)
        if arg == 'area':
            embed = discord.Embed(title="Area",
                                  description=f'''**Usage: `{prefix}area <country>`
        Returns the area of the country in `sq. km`**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url= main_url
                
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'capital':
            embed = discord.Embed(title="Capital",
                                  description='''**Usage: `.capital <country>`
        Returns the capital city of the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'currency':
            embed = discord.Embed(title="Currency",
                                  description=f'''**Usage: `{prefix}currency <country>`
        Returns the currency(s) used by the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'population':
            embed = discord.Embed(
                title="Population",
                description=f'''**Usage: `{prefix}population <country>`
        Returns the approximate population of the country**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'states':
            embed = discord.Embed(title="States/Provinces",
                                  description=f'''**Usage: `{prefix}states <country>`
        Returns the states/provinces in the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)
        elif arg == 'language':
            embed = discord.Embed(title="Language",
                                  description=f'''**Usage: `{prefix}language <country>`
        Returns the language(s) of the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'region':
            embed = discord.Embed(title="Region",
                                  description=f'''**Usage: `{prefix}region <country>`
        Returns the general region the country is located in**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'subregion':
            embed = discord.Embed(
                title="Subregion",
                description=f'''**Usage: `{prefix}subregion <country>`
        Returns the subregion the country is located in**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'timezone':
            embed = discord.Embed(title="Timezone",
                                  description=f'''**Usage: `{prefix}timezone <country>`
        Returns the timezone(s) located in the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'borders':
            embed = discord.Embed(title="Borders",
                                  description=f'''**Usage: `{prefix}borders <country>`
        Returns the countries that border the selected country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'coords':
            embed = discord.Embed(title="Coords",
                                  description=f'''**Usage: `{prefix}coords <country>`
        Returns the coordinates of the country. 
        A negative coordinate means south or west. 
        A positive coordinate means North or East.
        Longitude shows location horizontally
        Latitude shows location vertically
        Format: `Longitude, Latitude`**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'list':
            embed = discord.Embed(
                title="Borders",
                description=f'''**Usage: `{prefix}list <letter or letters>`
        Returns the countries that start with the selected letter or letters**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'gdp_percap':
            embed = discord.Embed(
                title="gdp_percap",
                description=f'''**Usage: `{prefix}gdp_percap <country> <year>`
        Returns the GDP per capita of the country in that year**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'gni_percap':
            embed = discord.Embed(
                title="gni_percap",
                description=f'''**Usage: `{prefix}gni_percap <country> <year>`
        Returns the GNI per capita of the country in that year**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'inflation':
            embed = discord.Embed(
                title="Inflation",
                description=f'''**Usage: `{prefix}inflation <country> <year>`
        Returns the percent of inflation of the country in that year.**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'covid':
            embed = discord.Embed(
                title="Covid 19 info",
                description=f'''**Usage: `{prefix}covid <country>`
        Returns information about the coronavirus for the country**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed = embed)
            
        elif arg == 'changeprefix':
          embed = discord.Embed(
                title="Change prefix",
                description=f'''**Usage: `{prefix}changeprefix <prefix>`
        Sets a new prefix. User needs to have admin to use this command.**''',
                color=0xFF5733)
          embed.set_thumbnail(
                url=
                main_url
            )

          await ctx.channel.send(embed = embed)

        elif arg == 'guess_capital':
            embed = discord.Embed(
                title="Guess the Capital",
                description=None,
                color=0xFF5733)
        
            embed.add_field(name = "Usage", value = f''' ```{prefix}guess_capital``` ***OR***```{prefix}guess_capital reverse```''', inline = False)

            embed.add_field(name = "Normal mode", value = '''A random country is given. Players will try to give the capital before the time rns out.''')

            embed.add_field(name="Reverse mode", value='''A capital city of a country is given. Players will try to give the country before the time runs out.''')

            embed.add_field(name="Things to Note", value='''Time limit must not exceed `300` seconds.
            Type `quit` while playing to quit the game. 
            Have Fun!!! 🤞''')
            
            

            embed.set_thumbnail(
                    url=
                    main_url
                )

            await ctx.channel.send(embed = embed)

        elif arg == 'work':
          embed=discord.Embed(title='Work', description=f'''**Usage: `{prefix}work`
          You worked for your country and got more people to live in it. Has a cooldown of 15 sec**''', color=Color.teal())

          
        
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)
        
        elif arg == 'flag':
          embed=discord.Embed(title='Flag', description=f'''**Usage: `{prefix}flag`
                          OR         `{prefix}flag <country>`
          Returns a flag of a random country**''', color=Color.teal())

          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)
        
        elif arg == 'store':
          embed=discord.Embed(title='Store', description=f'''**Usage: `{prefix}store`
          The store where you can buy upgrades for your country!**''', color=Color.teal())

          
        
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)
        
        elif arg == 'profile':
          embed=discord.Embed(title='Profile', description=f'''**Usage: `{prefix}profile`
          View stats about your country**''', color=Color.teal())

          
        
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)
        
        elif arg == 'start':
          embed=discord.Embed(title='Start', description=f'''**Usage: `{prefix}start`
            Start your country**''', color=Color.teal())

            
          
          embed.set_thumbnail(
                    url=
                    main_url
                )
            
          await ctx.channel.send(embed=embed)

        

        elif arg == 'stats':
            embed = discord.Embed(title="Stats",
                                  description=f'''**Usage: `{prefix}stats`
        Returns general information about the bot such as, `latency`, `server count`, and `memory usage`**''', color=0xFF5733)
            embed.set_thumbnail(
                url=
                main_url
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'quit':
          embed=discord.Embed(title='Quit', description=f'''**Usage: `{prefix}quit`
          You can use this command to quit your country.**''', color=Color.teal())

          
        
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)

        elif arg == 'change':
          embed=discord.Embed(title='Change', description=f'''**Usage: `{prefix}change <name>`
          Change your country name**''', color=Color.teal())

          
        
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)

        
        elif arg == 'buy':
          embed=discord.Embed(title='Buy', description=f'''**Usage: `{prefix}buy <ID> <amount>`
          Amount is only specified when buying multiplier boosts
          Buy uogrades for your country**''', color=Color.teal())

          
        
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)

        elif arg == 'daily':
          embed=discord.Embed(title='Daily', description=f'''**Usage: `{prefix}daily`
          Get 100 more people into your country every day. Has a 24 hour cooldown**''', color=Color.teal())

          
        
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)

        elif arg == 'youtube_search':
          embed=discord.Embed(title='Youtube Search', description=f'''**Usage: `{prefix}youtube_search <search query>`
          Returns information about a video based on thesearch query**''', color=Color.teal())

          embed.set_thumbnail(url=main_url)
          
          await ctx.channel.send(embed=embed)

        elif arg == 'color':
          embed=discord.Embed(title='Color', description=f'''**Usage: `{prefix}color <rgb or hex>`
          Returns information about the color you entered**''', color=Color.teal())
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)
        elif arg == 'war':
          embed=discord.Embed(title='War', description=f'''**Usage: `{prefix}war <user>`
          Wage war on another user**''', color=Color.teal())
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)
        elif arg == 'gift':
          embed=discord.Embed(title='Gift', description=f'''**Usage: `{prefix}gift <user> <amount>`
          Allows you to gift population to another user**''', color=Color.teal())
          embed.set_thumbnail(
                  url=
                  main_url
              )
          
          await ctx.channel.send(embed=embed)


        elif arg == 'coinflip':
          embed=discord.Embed(title='Coinflip', description=f''' [] = Optional <> = Mandatory
          **Usage: `{prefix}coinflip <heads | tails> [bet amount]`
          
          Allows you to gamble with your population.**''', color=Color.teal())
          embed.set_thumbnail(
                  url=
                  main_url
              )

          await ctx.channel.send(embed=embed)

        elif arg.lower() == 'changelog':
          embed=discord.Embed(title='Coinflip', description=f''' 
          **Usage: `{prefix}changelog`
          
        Shows the recent changes to the bot.**''', color=Color.teal())
          embed.set_thumbnail(
                  url=
                  main_url
              )

        elif arg.lower() == 'tax':
          embed = discord.Embed(title='Tax', description='''**Usage:** `.tax`
          tax your population to earn coins''', color=Color.teal())
          
          embed.set_thumbnail(
                  url=
                  main_url
              )

          await ctx.send(embed=embed)
          
          



      
        
        else:
            embed = discord.Embed(title="Country Bot Help",
                                  description=f'''**Prefix = `{db[ctx.guild.id]}`

        ```diff\n- Woops!, the command "{arg}" doesn't exist  
        ```
      
          Type `{db[ctx.guild.id]}help <command>` for more information on a specific  command.**
          
          '''.format(arg=arg),
                                  color=0xFF5733)

            embed.set_thumbnail(
              url=
                main_url
            )

            await ctx.channel.send(embed=embed)
    
        
    

if not os.getenv("TOKEN"):
  print("HEYYYYY. DONT TRY TO STEAL MY TOKEN OK")
  quit()
if __name__ == '__main__':
  start_extensions(bot)
  keep_alive.keep_alive()
  bot.run(os.getenv("TOKEN"))
