#imports form dicord.py

from discord.ext.commands import has_permissions
import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType


#imports for eval command
from pathlib import Path
import textwrap, contextlib
from traceback import format_exception




#imports for mongodb
import motor.motor_asyncio

#imports for data on countries
from countryinfo import CountryInfo
import country_converter as coco
import pycountry
import wbdata
from emojiflags.lookup import lookup

#imports for json
import json

#imports for checking text
from fuzzywuzzy import fuzz
import unicodedata
import regex as re

#other
import random
import resource, psutil
import time
import datetime
import requests
import io
import os, topgg
from dotenv import load_dotenv
load_dotenv()
#asyncio
import asyncio

#replit db

#internal imports
from mongomethods import *

#global vars
global main_url
global quiz_country_list
quiz_country_list = list(CountryInfo().all().keys())
main_url = 'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
global dic
dic = {1 : "Mom's basement", 2 : 'Apartment (with roomate)', 3 : 'Home Office', 5 : 'Mansion', 10 : 'Space Base'}
global username, password
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
global hunt_animals
hunt_animals = {'Boar': [':boar:', 1000], 'Deer': [':deer:', 400], 'Crocodile': [':crocodile:', 750]}
global cc
cc = coco.CountryConverter()
global main_up
main_up = time.time()








#getting the prefix of the guild from replit db
def get_prefix123(bot, msg):
    try:
      prefix = get_prefix2(msg.guild.id)
    except:
      create_prefix2(msg.guild.id, '.')
      return '.'
    return prefix
    

   
#creating bot instance


bot = commands.Bot(command_prefix=get_prefix123, case_insensitive=True, help_command=None)

dbl_token = os.environ['TOPGGTOKEN']





bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "dbl_password")
bot.topgg_webhook.run(4355)  # this method can be awaited as well




@bot.event
async def on_dbl_vote(data):
    """An event that is called whenever someone votes for the bot on Top.gg."""
    if data["type"] == "test":
        # this is roughly equivalent to
        # return await on_dbl_test(data) in this case
        return bot.dispatch('dbl_test', data)

    user = await bot.fetch_user(data['user'])
    try:
      a = await reading(user.id)
    except:
      await user.send("Thanks for voting! Unfortunately since you have not made a country, you can't redeem any rewards :( To create a country type `.start` Remember, replace `.` with the prefix of the bot in the server you are in!")
      return
    await update((user.id, a[0][0], a[0][1] + (1000 * (a[0][5] + 1)), a[0][2], a[0][3], a[0][4], a[0][10]))
    await update_coins((user.id, a[0][11] + (100 * a[0][5])))
    await user.send('Thanks for voting, I apreciate it! Check your profile to see the received rewards!')
    print(f"Received a vote:\n{data}")

@bot.event
async def on_dbl_test(data):
    """An event that is called whenever someone tests the webhook system for your bot on Top.gg."""
    user = await bot.fetch_user(data['user'])
    try:
      a = await reading(user.id)
    except:
      await user.send("Thanks for voting! Unfortunately since you have not made a country, you can't redeem any rewards :( To create a country type `.start` Remember, replace `.` with the prefix of the bot in the server you are in!")
      return
    await update((user.id, a[0][0], a[0][1] + (1000 * (a[0][5] + 1)), a[0][2], a[0][3], a[0][4], a[0][10]))
    await update_coins((user.id, a[0][11] + (100 * (a[0][5] + 1))))
    await user.send('Thanks for voting, I apreciate it! Check your profile to see the received rewards!')
    print(f"Received a test vote:\n{data}")



#add guild id to replit db when bot is added
@bot.event
async def on_guild_join(guild):
  await create_prefix(guild.id, '.')
#eremov guild id from replit db when bot is kicked
@bot.event
async def on_guild_remove(guild):
  await delete_prefix(guild.id)





 
  
#A command to change the prefix of the bot in that guild


def start_extensions(bot):
  bot.load_extension("extensions.adminstuff")
  #bot.load_extension("extensions.topgg")
  bot.load_extension("extensions.misc")
  bot.load_extension("extensions.country_database")
  bot.load_extension("extensions.gambling")
  bot.load_extension("extensions.economy")
  bot.load_extension("extensions.memes")
  bot.load_extension("extensions.games")
  bot.load_extension("extensions.general")
  bot.load_extension("extensions.help_page")
  bot.load_extension("extensions.topgg")
  bot.load_extension("jishaku")







@bot.command(aliases=['lb'])
async def leaderboard(ctx, *arg):

  if len(arg) == 0:

    data = await find_lb()
    
    

    for i in data:
      i['_id'] =  await bot.fetch_user(int(i['_id']))
    
    string = ''''''
    for x, i in enumerate(data, start=1):
      prestige = i['data']['prestige']
      name = i['_id']
      name2 = i['data']['name']
      string = string + f'**{x}.** {name}: `{name2}`| `Prestige Level {prestige}`\n'

    embed = discord.Embed(title='Global Leaderboard (prestige)', description=string)
    await ctx.send(embed=embed)

  elif len(arg) == 1:

    if arg[0] == 'coins':
      data = await find_lb2()
      
      

      for i in data:
        i['_id'] =  await bot.fetch_user(int(i['_id']))
      
      string = ''''''
      for x, i in enumerate(data, start=1):
        prestige = i['data']['coins']
        name = i['_id']
        name2 = i['data']['name']
        string = string + f'**{x}.** {name}: `{name2}`| `{prestige}` :coin:\n'

      embed = discord.Embed(title='Global Leaderboard (prestige)', description=string)
      await ctx.send(embed=embed)

  else:
    await ctx.send(':x: uhhhhhh thats not not an option')

@leaderboard.error
async def lb_error(ctx, error):
  raise error


@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def hunt(ctx):
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
async def hunt_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="Hey!",description=f'''You can't hunt right now! Try again in `{error.retry_after:.2f}`s.''')
        await ctx.send(embed=em) 

@bot.command()
async def sell(ctx, *item1):
  try:
    a = await find_inventory(ctx.author.id)
    ab = await reading(ctx.author.id)

  except:
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Hey!', description=f'You dont have a country! Type `{prefix}start` to start your country!')
    await ctx.send(embed=embed)
    return

  if len(item1) == 0:
    prefix = await get_prefix(ctx.guild.id)
    await ctx.send(embed=discord.Embed(title='Bad Usage', description=f'''[] = optional
    <> = mandatory
    Invalid Usage: ```{prefix}sell <item> [amount]```'''))
    return

  if len(item1) == 1:
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


    

    

    

    



    

@bot.command(aliases=['inv'])
async def inventory(ctx):
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







  #command to get information about the bot



      


  


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
[{await count()}]
```''')

  embed.add_field(name='Creator', value=f'''```ini
[Coder N#0001]
```''', inline=True)

  embed.add_field(name='Websocket Ping', value=f'''```ini
[{bot.latency * 1000} ms]
```''')

  embed.add_field(name='Commands', value=f'''```css
[{len(bot.commands)}]
```''')




  embed.set_footer(text='If some percentages show 0.0%, it means that the number is really close to zero.')
  await ctx.channel.send(embed=embed)



async def presence():
  while True:
      await bot.change_presence(activity=discord.Game(name=".help"))
      await asyncio.sleep(10)
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="@Country Bot prefix"))
      await asyncio.sleep(10)
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} guilds"))
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

  



  

    



#setting the status of the bot and sending a message if the guild is not in db

async def refugee_drops():


  words = ['come here!', 'more people!', '🙂', "hello!"]

 

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
            a = await reading(msg.author.id)
          except:
            embed = discord.Embed(title='Sorry', description=f":x: You don't have a country. Type `.start` to start one")
            await msg.channel.send(embed=embed)
            n = True

          await update((msg.author.id, a[0][0], a[0][1] + amount, a[0][2], a[0][3], a[0][4], a[0][10]))
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


'''for i in bot.guilds:
      if str(i.id) not in db:
        for channel in i.channels:
            if channel.type == discord.ChannelType.text:
              main_channel =  bot.get_channel(channel.id)
              print('OfflINE')
              try:
                await main_channel.send("To continue using this bot, please `kick` it and `add it again`. This could have been caused because the `bot was added when it was offline`.")
                break
              except:
                pass'''
      
@bot.event
async def on_ready():  
    global task
    print('hi')
    task = bot.loop.create_task(refugee_drops())
    bot.loop.create_task(presence())
    print('bot is ready')
    print(f"bot is in {len(bot.guilds)} servers")


#commands for the bot


#listening for the message that users send if they forgot their prefix

@bot.listen()
async def on_message(msg):

  if msg.content == f'<@810662403217948672> prefix' or msg.content == f'<@!810662403217948672> prefix':
        prefix = await get_prefix(msg.guild.id)
        await msg.channel.send(f"My prefix in this server is `{prefix}`")

  elif msg.content == f'<@810662403217948672>prefix' or msg.content == f'<@!810662403217948672>prefix':
        prefix = await get_prefix(msg.guild.id)
        await msg.channel.send(f"My prefix in this server is `{prefix}`")

  elif msg.content == '<@810662403217948672>' or msg.content == '<@!810662403217948672>':
        prefix = await get_prefix(msg.guild.id)
        await msg.channel.send(f"My prefix in this server is `{prefix}`")
  
  

  



    
  


    




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

  



#a command to give the capital of a country



  



  
  



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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}population <country>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}area <country>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}states <country>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}language <country>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}region <country>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}subregion <country>```')
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

    await writing((ctx.author.id, msg.content, 0, 1, "Mayor", 1, 0, 1000000000, 0, 0, 0, 0, 0))

    await ctx.channel.send('Hooray, Country Created!!!!')
  except:
    embed = discord.Embed(title='Sorry', description=''':x: You already have a country.''')

    await ctx.channel.send(embed=embed)


@bot.command()
@commands.is_owner()
async def send_update(ctx, *, info):
  embed = discord.Embed(title='Update!!!', description=info)
  for i in findall():
    await bot.get_channel(i["_id"]).send(embed=embed)

@bot.command()
@has_permissions(administrator=True)
async def configurechannel(ctx, channel):
  channel = channel.strip('<')
  channel = channel.strip('>')
  channel = channel.strip('#')
  
  try:
    await bot.get_channel(int(channel)).send(embed=discord.Embed(title='Success', description='Channel is configured to receive updates about the bot!'))

  except Exception as e:
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

   elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}configurechannel <channel>```')
    await ctx.channel.send(embed=embed)

   


@bot.command()
@has_permissions(administrator=True)
async def unconfigurechannel(ctx, channel):
  channel = channel.strip('<')
  channel = channel.strip('>')
  channel = channel.strip('#')
  try:
    await delete_update(int(channel))

  except Exception as e:
    await ctx.send(embed=discord.Embed(title='Oh No!', description=":x: Please provide a valid channel!"))
    return

  await ctx.send(embed=discord.Embed(title='Success', description=f"<#{channel}> won't receive update messages"))

@unconfigurechannel.error
async def unconfigure_error(ctx, error):
   if isinstance(error, discord.ext.commands.MissingPermissions):
       await ctx.send("You need the `ADMINISTRATOR` permission to do that!")

   elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}unconfigurechannel <channel>```')
    await ctx.channel.send(embed=embed)

@bot.command()
async def profile(ctx, member: discord.Member=None):
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
  

@bot.command(aliases=['shop'])
async def store(ctx):
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
@bot.command()
async def work(ctx):
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
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="Too tired",description=f'''You are too tired to work again. You can work in `{error.retry_after:.2f}`s.''')
        await ctx.send(embed=em)

    


@bot.command()
async def prestige(ctx):
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
        msg = await bot.wait_for('message', check=check, timeout=100)

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
    
@bot.command()
async def quit(ctx):
  prefix = await get_prefix(ctx.guild.id)
  embed = discord.Embed(title='quit', description=':x: Are you really sure you want to quit your country. You will lose all your data (`y`,`n`)')
  await ctx.channel.send(embed=embed)
  thechannel = ctx.channel
  theauthor = ctx.message.author
  def check(m):
    return m.content == 'y' or m.content == 'n' and m.channel == thechannel and m.author == theauthor 
  msg = await bot.wait_for('message', check=check, timeout=100)
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


@bot.command()
async def buy(ctx, *id):
  prefix = await get_prefix(ctx.guild.id)
  try:
    a = await reading(ctx.message.author.id)
  except:
    
    embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{prefix}start`''')
    await ctx.channel.send(embed=embed)
  if len(id) == 0:
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}buy <ID> <amount>```')
    await ctx.channel.send(embed=embed)
    return

  
  if len(id) == 2:
    amount = id[1]
    amount = amount.strip(',')

    try:
      int(amount)
    except:
      await ctx.send(':x: uhhhh. Thats not a valid amount')

    

    if id[0] == '1':
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

      

      

  elif len(id) == 1:
    if id[0] == '1':
      embed = discord.Embed(title='Error', description=':x: How much multiplier are you buying!')
      await ctx.channel.send(embed=embed)

    elif id[0] == '2':
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

    elif id[0] == '3':
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

    elif id[0] == '4':
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
    
    elif id[0] == '5':
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



      

@bot.command()
async def gift(ctx, user1, amount):

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

    

  

  

@bot.command()
async def change(ctx, *, arg):
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

@change.error
async def change_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}change <new country name>```')
    await ctx.channel.send(embed=embed)

@commands.cooldown(1, 86400, commands.BucketType.user)
@bot.command()
async def daily(ctx):
  try:
    a = await reading(ctx.message.author.id)
  except:
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Ummmmm...', description = f'''You anyways don't even have a country. Create one with `{prefix}start`''')
    
  a = await reading(ctx.message.author.id)
  await update((ctx.message.author.id, a[0][0], a[0][1] + (100 * ((a[0][1]**0.5)/100)) * (a[0][5] +1), a[0][2], a[0][3], a[0][4], a[0][10]))

  

  embed = discord.Embed(title='Daily', description=f'`100` more people joined your country!! Your new population is `{a[0][1] + 100}`')

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
      prefix = await get_prefix(ctx.guild.id)
      embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}gift <user> <amount>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}timezone <country>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}borders <country>```')
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
            description="** We could not find data for {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}coords <country>```')
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}covid <country>```')
    await ctx.channel.send(embed=embed)

#city_weather command





@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
      main_message = ctx.message.content.split(' ')[0]
      
      similar = []
      other=[]
      
      prefix = await get_prefix(ctx.guild.id)

      for commands in bot.commands:
        
        if fuzz.ratio(main_message, commands.name) > 50:
          similar.append(f'`{prefix}{commands.name}`')
          other.append(commands)
      
      
      if len(similar) == 0:
        return
      similar = ' '.join(similar)

      
     
      
    
      await ctx.channel.send(f"Did you mean {similar}")

    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
       pass

    

    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
      
      await ctx.author.send(":thinking: Something went wrong... Double check that I have permission to talk there.")
      raise error
      

    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
      pass
    

    else:
       raise error





if not os.getenv("TOKEN"):
  print("HEYYYYY. DONT TRY TO STEAL MY TOKEN OK")
else:
  if __name__ == '__main__':
    start_extensions(bot)
    bot.run(os.getenv("TOKEN"))