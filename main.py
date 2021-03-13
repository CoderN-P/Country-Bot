#importing dependecies
import discord
import regex as re
import keep_alive
from countryinfo import CountryInfo
from discord.ext import commands
import country_converter as coco
import pycountry
from pycountry import languages, currencies
from datetime import datetime
import requests
import json
import matplotlib.pyplot as plt
import ast
import wbdata
import pandas as pd
import random
import time
global cc
from replit import db
from fuzzywuzzy import fuzz
import asyncio, os
import operator
from emojiflags.lookup import lookup

# Initialize the AWOC class.
country_list = CountryInfo().all().keys()
#getting a list of all countries, for the guess_capital command
global country_list1
country_list1 = [key for key in CountryInfo().all()]

#getting the prefix of the guild from the JSON file
def get_prefix(bot, msg):
    prefixes = db[str(msg.guild.id)]

    return prefixes
  

  



    
      

#Initiating flask app
keep_alive.keep_alive()


#initiating country_converter
cc = coco.CountryConverter()

#initiating the bot
bot = commands.Bot(command_prefix=get_prefix, help_command=None)









#add guild.id to JSON file on guild join

@bot.event
async def on_guild_join(guild):
  db[guild.id] = '.'

#remove guild.id from JSON file on guild remove
@bot.event
async def on_guild_remove(guild):
  del db[guild.id]

#A command to change the prefix of the bot in that guild

@bot.command()
async def changeprefix(ctx, prefix):
  if ctx.message.author.guild_permissions.administrator:
    db[ctx.guild.id] = prefix

    await ctx.channel.send(f"Prefix has been changed to `{prefix}`")
  else:
    await ctx.channel.send("You don't have sufficient permissions to do that")

#getting the prefix of the guild


#setting the status of the bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=".help"))
    print('bot is ready')

#commands for the bot

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

  

  if len(arg) == 0:
    count = 0
    bol = True
    while bol:

      random_country = random.choice(country_list1)

      country_capital1 = CountryInfo(random_country)

      country_capital = country_capital1.capital()

      #try:

      result4 = coco.convert(names=random_country, to='ISO2')

      await ctx.channel.send(f"What is the capital of....... `{random_country}` {lookup(result4)}")

      #except:
        #await ctx.channel.send(f"What is the capital of....... `{random_country}`")


      

      

      def check(m):
        return fuzz.ratio(country_capital.lower(), m.content.lower()) > 82 and m.channel == channel

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

      

      
      
      
   

  

  if len(arg) == 1:
    count = 0
    bol = True
    while bol:

      random_country = random.choice(country_list1)

      country_capital1 = CountryInfo(random_country)

      country_capital = country_capital1.capital()

      #try:

      result4 = coco.convert(names=random_country, to='ISO2')

      await ctx.channel.send(f"What Country has `{country_capital}` as its capital. Here is a hint: {lookup(result4)}")

      #except:
        #await ctx.channel.send(f"What is the capital of....... `{random_country}`")


     

      

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
  




@bot.command(name='capital')
async def cap(ctx, *, country):

    try:
    
      print(country)
      if fuzz.ratio(country, "England") > 80:
        country1 = CountryInfo('Great Britan')
      else:
        country1 = CountryInfo(country)

      result = country1.capital()

      print(country)

      embed = discord.Embed(
              title="Capital of " + country,
              description="**The capital of {country} is {result}**".format(
                  result=result, country=country),
              color=0xFF5733)

      result4 = coco.convert(names=country, to='ISO2')
      embed.set_thumbnail(
              url='https://www.countryflags.io/{}/flat/64.png'.format(result4))

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
            description='**{result1}**'.format(result1=result1),
            color=0xFF5733)

        result4 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{}/flat/64.png'.format(result4))

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


@bot.command()
async def area(ctx, *, country):
    try:
        country1 = CountryInfo(country)
        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")
        result = country1.area()

        result1 = "{:,}".format(result)
        result1 = str(result1)
        result2 = result1 + ' sq. km'

        embed = discord.Embed(
            title="Area of " + country,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        result4 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{}/flat/64.png'.format(result4))

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


@bot.command()
async def currency(ctx, *, country):
    try:
        country1 = CountryInfo(country)
        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.currencies()
        result5 = []
        if result == ['USD', 'USN', 'USS']:
            result.pop(1)
            result.pop(1)

        for i in range(0, len(result)):

            result4 = pycountry.currencies.get(alpha_3=result[i])

            result5.append(result4.name)

        result1 = " |".join(result5)
        result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

        embed = discord.Embed(
            title="Currency(s) of " + country,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        result4 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{}/flat/64.png'.format(result4))

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


@bot.command()
async def states(ctx, *, country):
    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.provinces()

        result1 = " |".join(result)

        result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

        embed = discord.Embed(
            title="States of " + country,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        result4 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{}/flat/64.png'.format(result4))

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
                url='https://www.countryflags.io/{}/flat/64.png'.format(
                    result4))

            embed.set_footer(
                text="Requested by: {name}".format(name=ctx.message.author),
                icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Language(s) of " + country,
                description='**{result2}**'.format(result2=result2),
                color=0xFF5733)

            result4 = coco.convert(names=country, to='ISO2')
            embed.set_thumbnail(
                url='https://www.countryflags.io/{}/flat/64.png'.format(
                    result4))

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


@bot.command()
async def region(ctx, *, country):

    try:
        country1 = CountryInfo(country)
        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.region()

        embed = discord.Embed(title="Region for " + country,
                              description='**{result}**'.format(result=result),
                              color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                result3=result3))

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


@bot.command()
async def subregion(ctx, *, country):

    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.subregion()

        embed = discord.Embed(title="Subregion for " + country,
                              description='**{result}**'.format(result=result),
                              color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                result3=result3))

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


@bot.command()
async def timezone(ctx, *, country):
    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.timezones()

        result1 = " |".join(result)

        result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

        embed = discord.Embed(
            title="Timezone(s) of " + country,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                result3=result3))

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


@bot.command()
async def borders(ctx, *, country):
    try:
        country1 = CountryInfo(country)

        if country == 'england' or country == 'England':
            country1 = CountryInfo("Great Britain")

        result = country1.borders()

        result1 = cc.convert(names=result, to='name_short', not_found=False)

        if isinstance(result1, str) == True:
            result2 = []
            result2.append(result1)
            result3 = " |".join(result2)

            result4 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result3)

            if not result4:
                embed = discord.Embed(
                    title="Borders of " + country,
                    description=
                    '**There are no countries {country} borders :(**'.format(
                        country=country),
                    color=0xFF5733)

                result5 = coco.convert(names=country, to='ISO2')
                embed.set_thumbnail(
                    url='https://www.countryflags.io/{}/flat/64.png'.format(
                        result5))

                embed.set_footer(text="Requested by: {name}".format(
                    name=ctx.message.author),
                                 icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Borders of " + country,
                    description='**{result4}**'.format(result4=result4),
                    color=0xFF5733)

                result5 = coco.convert(names=country, to='ISO2')
                embed.set_thumbnail(
                    url='https://www.countryflags.io/{}/flat/64.png'.format(
                        result5))

                embed.set_footer(text="Requested by: {name}".format(
                    name=ctx.message.author),
                                 icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)

        elif type(result1) == type([]):
            result2 = " |".join(result1)

            result3 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result2)
            print('hi')

            if not result3:
                embed = discord.Embed(
                    title="Borders of " + country,
                    description=
                    '**There are no countries {country} borders :(**'.format(
                        country=country),
                    color=0xFF5733)

                result5 = coco.convert(names=country, to='ISO2')
                embed.set_thumbnail(
                    url='https://www.countryflags.io/{}/flat/64.png'.format(
                        result5))

                embed.set_footer(text="Requested by: {name}".format(
                    name=ctx.message.author),
                                 icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Borders of " + country,
                    description='**{result3}**'.format(result3=result3),
                    color=0xFF5733)

                result5 = coco.convert(names=country, to='ISO2')
                embed.set_thumbnail(
                    url='https://www.countryflags.io/{}/flat/64.png'.format(
                        result5))

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
            description='**{country} is located at the coordinates: {result2}**'
            .format(result2=result2, country=country),
            color=0xFF5733)

        result3 = coco.convert(names=country, to='ISO2')
        embed.set_thumbnail(
            url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                result3=result3))

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


@bot.command()
async def list(ctx, arg):

    check = arg
    new_list = []
    print(pycountry.countries)
    for x in pycountry.countries:
        s = x.name
        if re.match(check, s, re.I):
            new_list.append(x.name)

    seen = {}
    dupes = []

    for x in new_list:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
                new_list.pop(index(x))
            seen[x] += 1

    print(dupes)
    print(new_list)

    result1 = " |".join(new_list)

    result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

    print(new_list)

    if not result2:
        embed = discord.Embed(
            title="Sorry",
            description='**there are no countries starting with {}**'.format(
                arg),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

    else:
        embed = discord.Embed(
            title="Countries starting with " + arg,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        await ctx.channel.send(embed=embed)

@bot.command()
async def gdp_percap(ctx, *, arg):
  try:
    country1 = coco.convert(names=arg, to='iso2')
    country1 = country1.upper()
    country2 = []
    country2.append(country1)
    print(country2)
    
    
    indicators = {'NY.GDP.PCAP.CD':'GDP per Capita'}
    
    #grab indicators above for countires above and load into data frame
    df = wbdata.get_dataframe(indicators, country=country2, convert_date=False)
    
    
    
    
    df.plot(style='.-')
    plt.ylabel("GDP per capita in $USD")
    plt.title("GDP per capita of {} in $USD".format(arg))
    plt.savefig('gdp.png')
    
    plt.close()

    embed = discord.Embed(
              title="GDP per capita of {}".format(arg),
              description=None,
              color=0xFF5733)
    
    

    chart = discord.File("gdp.png")
    
    embed.set_image(url='attachment://gdp.png')

    result3 = coco.convert(names=arg, to='ISO2')
    embed.set_thumbnail(
              url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                  result3=result3))

    embed.set_footer(text="Information requested by: {}".format(
    ctx.message.author))

    await ctx.channel.send(embed=embed, file=chart)

  except:
      embed = discord.Embed(
            title="Sorry",
            description="**{} is not a country**".format(
                arg),
            color=0xFF5733)

      embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

      await ctx.channel.send(embed=embed)

  



@bot.command()
async def gni_percap(ctx, *, arg):
  try:
    country1 = coco.convert(names=arg, to='iso2')
    country2 = []
    country2.append(country1)
    
    
    
  
    #set up the indicator I want (just build up the dict if you want more than one)
    indicators = {'NY.GNP.PCAP.CD':'GNI per Capita'}
    
    #grab indicators above for countires above and load into data frame
    df = wbdata.get_dataframe(indicators, country=country2, convert_date=False)

    

    # a simple matplotlib plot with legend, labels and a title
    df.plot(style='.-'); 
    plt.legend(loc='best'); 
    plt.title("GNI Per Capita ($USD, Atlas Method)"); 
    plt.xlabel('Date'); plt.ylabel('GNI Per Capita ($USD, Atlas Method');
    plt.savefig('gni.png')
    plt.close()

    embed = discord.Embed(
              title="GNI per capita of {}".format(arg),
              description=None,
              color=0xFF5733)
    
    

    chart = discord.File("gni.png")
    
    embed.set_image(url='attachment://gni.png')

    result3 = coco.convert(names=arg, to='ISO2')
    
    embed.set_thumbnail(
                url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                    result3=result3))

    embed.set_footer(text="Information requested by: {}".format(
    ctx.message.author))

    await ctx.channel.send(embed=embed, file=chart)
  
  except:
        embed = discord.Embed(
            title="Sorry",
            description="**{} is not a country**".format(arg),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

@bot.command()
async def inflation(ctx, *, arg):

  try:
    country1 = coco.convert(names=arg, to='iso2')
    country2 = []
    country2.append(country1)
    
    
    
  
    #set up the indicator I want (just build up the dict if you want more than one)
    indicators = {'NY.GDP.DEFL.KD.ZG': 'Inflation (annual %)'}  
    
    #grab indicators above for countires above and load into data frame
    df = wbdata.get_dataframe(indicators, country=country2, convert_date=False)

    

    # a simple matplotlib plot with legend, labels and a title
    df.plot(style='.-'); 
    plt.legend(loc='best'); 
    plt.title("Inflation (annual %)"); 
    plt.xlabel('Date'); plt.ylabel('Inflation (annual %)');
    plt.savefig('inflate.png')
    plt.close()

    embed = discord.Embed(
              title="Inflation of {}".format(arg),
              description=None,
              color=0xFF5733)
    
    

    chart = discord.File("inflate.png")
    
    embed.set_image(url='attachment://inflate.png')

    result3 = coco.convert(names=arg, to='ISO2')
    
    embed.set_thumbnail(
                url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                    result3=result3))

    embed.set_footer(text="Information requested by: {}".format(
    ctx.message.author))

    await ctx.channel.send(embed=embed, file=chart)

  except:
    embed = discord.Embed(
    title="Sorry",
    description="**{} is not a country**".format(
                arg),
            color=0xFF5733)

    embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg')

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
    
    
    embed = discord.Embed(
              title="Covid19 info for " + arg,
              description=f'''**New cases: {new_cases}
                              Active cases: {active_cases}
                              Critical cases: {critical_cases}
                              Recovered: {recovered}
                              Cases per 1 million people: {cases_per1mill}
                              Total cases: {total_cases}**''',
              color=0xFF5733)

    result3 = coco.convert(names=arg, to='ISO2')
    embed.set_thumbnail(
              url='https://www.countryflags.io/{result3}/flat/64.png'.format(
                  result3=result3))

    embed.set_footer(text="Information requested by: {}".format(
              ctx.author.display_name))

    await ctx.channel.send(embed=embed)

  except:
    embed = discord.Embed(title="Sorry",description="**We could not find data for {}**".format(arg), color=0xFF5733)

    embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

    await ctx.channel.send(embed=embed)

#city_weather command

@bot.command()
async def city_weather(ctx, *, arg):
    # Python program to find current  
  # weather details of any city 
  # using openweathermap api 
    
  # import required modules 

    
  # Enter your API key here 
  api_key = "77fe8413f4f97c04a4d72d48c3d0d890"
    
  # base_url variable to store url 
  base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
  # Give city name 

    
  # complete_url variable to store 
  # complete url address 
  complete_url = base_url + "appid=" + api_key + "&q=" + arg 
    
  # get method of requests module 
  # return response object 
  response = requests.get(complete_url) 
    
  # json method of response object  
  # convert json format data into 
  # python format data 
  x = response.json() 
    
  # Now x contains list of nested dictionaries 
  # Check the value of "cod" key is equal to 
  # "404", means city is found otherwise, 
  # city is not found 
  if x["cod"] != "404": 
    
      # store the value of "main" 
      # key in variable y 
      y = x["main"] 
    
      # store the value corresponding 
      # to the "temp" key of y 
      current_temperature = y["temp"] 
    
      # store the value corresponding 
      # to the "pressure" key of y 
      current_pressure = y["pressure"] 
    
      # store the value corresponding 
      # to the "humidity" key of y 
      current_humidity = y["humidity"] 
    
      # store the value of "weather" 
      # key in variable z 
      z = x["weather"] 
    
      # store the value corresponding  
      # to the "description" key at  
      # the 0th index of z 
      weather_description = z[0]["description"] 
    
      # print following values 

      current_temperature = (((int(current_temperature) - 273) * 1.8) + 32)

      embed = discord.Embed(
              title=f"Weather of {arg}",
              description=f'''** Temperature =  {str(current_temperature)}°F 
            \n Atmospheric pressure (in hPa unit) = {str(current_pressure)}
            \n Humidity (in percentage) = {str(current_humidity)}
            \n Description = {str(weather_description)}**''', color=0xFF5733)

      

      embed.set_footer(text="Information requested by: {}".format(
              ctx.message.author))

      await ctx.channel.send(embed=embed)
  
  else: 
    print(" City Not Found ") 








    

  

#Help Page    


@bot.command()
async def help(ctx, *arg):
    if len(arg) == 0:
        embed = discord.Embed(title="Country Bot Help",
                              description=f'''**Prefix = `{db[ctx.guild.id]}`
      
           Type `{db[ctx.guild.id]}help <command>` for more information on a specific  command.**

      ''',
                              color=0xFF5733)

        embed.add_field(
                name='Commands 📋',
                value='Use these commands to learn all about countries :smile:',
                inline=False)

        embed.add_field(
                name=':map: Geographical info',
                value=
                "`area`, `borders`,`coords`, `region`,       `subregion`, `timezone`",
                inline=True)

        embed.add_field(
                name=':information_source: General info',
                value="`capital`, `population`, `states`, `language`, `covid`, `city_weather`",
                inline=True)

        embed.add_field(name=':moneybag: Economy', value='`currency`, `gni_percap`, `gdp_percap`, `inflation`', inline=True)

        embed.add_field(name=':scroll: Country Database',
                            value='`list`',
                            inline=True)

        embed.add_field(name=':lock: Needs admin permissions', value='`changeprefix`', inline=True)

        embed.add_field(name=':video_game: Games', value='`guess_capital`', inline=True)


        embed.set_thumbnail(
            url=
            'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
        )

        await ctx.channel.send(embed=embed)

    if len(arg) == 1:
        arg = ' '.join(arg)
        if arg == 'area':
            embed = discord.Embed(title="Area",
                                  description=f'''**Usage: `{prefix}area <country>`
         Returns the area of the country in `sq. km`**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'capital':
            embed = discord.Embed(title="Capital",
                                  description='''**Usage: `.capital <country>`
         Returns the capital city of the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'currency':
            embed = discord.Embed(title="Currency",
                                  description=f'''**Usage: `{prefix}currency <country>`
         Returns the currency(s) used by the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
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
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'states':
            embed = discord.Embed(title="States/Provinces",
                                  description=f'''**Usage: `{prefix}states <country>`
         Returns the states/provinces in the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed=embed)
        elif arg == 'language':
            embed = discord.Embed(title="Language",
                                  description=f'''**Usage: `{prefix}language <country>`
         Returns the language(s) of the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'region':
            embed = discord.Embed(title="Region",
                                  description=f'''**Usage: `{prefix}region <country>`
         Returns the general region the country is located in**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
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
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'timezone':
            embed = discord.Embed(title="Timezone",
                                  description=f'''**Usage: `{prefix}timezone <country>`
         Returns the timezone(s) located in the country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'borders':
            embed = discord.Embed(title="Borders",
                                  description=f'''**Usage: `{prefix}borders <country>`
         Returns the countries that border the selected country**''',
                                  color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
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
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
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
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )
            await ctx.channel.send(embed=embed)

        elif arg == 'gdp_percap':
            embed = discord.Embed(
                title="gdp_percap",
                description=f'''**Usage: `{prefix}gdp_percap <country>`
         Returns the GDP per capita of the country over time. 
         Is shown in a line graph**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'gni_percap':
            embed = discord.Embed(
                title="gni_percap",
                description=f'''**Usage: `{prefix}gni_percap <country>`
         Returns the GNI per capita of the country over time. 
         Is shown in a line graph**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed=embed)

        elif arg == 'inflation':
            embed = discord.Embed(
                title="Inflation",
                description=f'''**Usage: `.{prefix}inflation <country>`
         Returns the percent of inflation of the country over time. 
         Is shown in a line graph**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
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
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed = embed)

        elif arg == 'city_weather':
            embed = discord.Embed(
                title="City Weather",
                description=f'''**Usage: `{prefix}city_weather <country>`
         Returns the approximate weather for that city**''',
                color=0xFF5733)
            embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed = embed)

        elif arg == 'changeprefix':
          embed = discord.Embed(
                title="Change prefix",
                description=f'''**Usage: `.{prefix} <prefix>`
        Sets a new prefix. User needs to have admin to use this command.**''',
                color=0xFF5733)
          embed.set_thumbnail(
                url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
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

            embed.add_field(name="Things to Note", value='''Time limit must not exceed `300` seconds. Have Fun!!! 🤞''')
            
            

            embed.set_thumbnail(
                    url=
                    'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
                )

            await ctx.channel.send(embed = embed)

        


        

        else:
            embed = discord.Embed(title="Country Bot Help",
                                  description=f'''**Prefix = `{db[ctx.guild.id]}`

        ```diff\n- Woops!, the command "{arg}" doesn't exist  
        ```
      
           Type `{db[ctx.guild.id]}help <command>` for more information on a specific  command.**
           
           '''.format(arg=arg),
                                  color=0xFF5733)

            embed.add_field(
                name='Commands 📋',
                value='Use these commands to learn all about countries :smile:',
                inline=False)

            embed.add_field(
                name=':map: Geographical info',
                value=
                "`area`, `borders`,`coords`, `region`,       `subregion`, `timezone`",
                inline=True)

            embed.add_field(
                name=':information_source: General info',
                value="`capital`, `population`, `states`, `language`, `covid`, `city_weather`",
                inline=True)

            embed.add_field(name=':moneybag: Economy', value='`currency`, `gni_percap`, `gdp_percap`, `inflation`', inline=True)

            embed.add_field(name=':scroll: Country Database',
                            value='`list`',
                            inline=True)

            embed.add_field(name=':lock: Needs admin permissions', value='`changeprefix`', inline=True)

            embed.add_field(name=':video_game: Games', value='`guess_capital`', inline=True)

            embed.set_thumbnail(
               url=
                'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'
            )

            await ctx.channel.send(embed=embed)



if not os.getenv("TOKEN"):
  print("HEYYYYY. DONT TRY TO STEAL MY TOKEN OK")
else:
  bot.run(os.getenv("TOKEN"))
