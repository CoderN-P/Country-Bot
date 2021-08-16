import discord
from discord.ext import commands
import country_converter as coco
import datetime
import wbdata
import pycountry
import re
from main import country_filter
import requests
from discord_slash import cog_ext
from fuzzywuzzy import fuzz

cc = coco.CountryConverter()
url = 'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'

class CountryEconomy2(commands.Cog, name='Economy Data (slash)', description="Commands that give you data about a country's economy."):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(description='Get the general currency of a real country.')
  async def currency(self, ctx, *, country: str):
      data = await country_filter(country, ctx)
      if data is None:
              return
      name = data['name']
      alpha2 = data['alpha2Code']
      alpha3 = data['alpha3Code']
      string = ''
      for i in data['currencies']:
              code = i['code']
              name2 = i['name']
              symbol = i['symbol']
              string += f'```{code} {name2} {symbol}``` '
      
      embed = discord.Embed(title=f'Currency of {name} — {alpha2} | {alpha3}', description=string, color=0xFF5733)
      embed.set_thumbnail(
              url=f'https://flagcdn.com/w80/{alpha2.lower()}.jpg')

      embed.set_footer(
              text="Requested by: {name}".format(name=ctx.author),
              icon_url=ctx.author.avatar_url)

      await ctx.send(embed=embed)


  @cog_ext.cog_slash(description='Get the gdp per capita of a real country in a certain year.')
  async def gdp_percap(self, ctx, country: str, year: int):
    arg = country
    arg2 = str(year)
    try:
      country1 = coco.convert(names=arg, to='iso2')
      country1 = country1.upper()
      country2 = []
      country2.append(country1)
      
      
      
      indicators = {'NY.GDP.PCAP.CD':'GDP per Capita'}
      
      #grab indicators above for countires above and load into data frame
      df = wbdata.get_dataframe(indicators, country=country2, convert_date=False).to_dict()['GDP per Capita'][arg2]
      
    
      
      if str(df) == 'nan':
        embed = discord.Embed(
            title="Sorry",
              description="**We couldn't find data for that year**".format(
                  arg),
              color=0xFF5733)

        embed.set_thumbnail(
              url=url
          )
        await ctx.send(embed=embed)
      else:
        embed = discord.Embed(
                  title="GDP per capita of {}".format(arg),
                  description=f'The gdp per capita of {arg} in {arg2} is/was $`{df}`',
                  color=0xFF5733)
        
        


        result3 = coco.convert(names=arg, to='ISO2')
        embed.set_thumbnail(
              url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

        embed.set_footer(text="Information requested by: {}".format(
        ctx.author))

        await ctx.send(embed=embed)

    except:
        embed = discord.Embed(
              title="Sorry",
              description="** We could not find data for that year**",
              color=0xFF5733)

        embed.set_thumbnail(
              url=url
          )

        await ctx.send(embed=embed)


  @cog_ext.cog_slash(description='Get the gni per capita of a real country.')
  async def gni_percap(self, ctx, country: str, year: int):
    arg = country
    arg2 = str(year)
    try:
      country1 = coco.convert(names=arg, to='iso2')
      country2 = []
      country2.append(country1)
      
      
      
    
      #set up the indicator I want (just build up the dict if you want more than one)
      indicators = {'NY.GNP.PCAP.CD':'GNI per Capita'}
      
      #grab indicators above for countires above and load into data frame
      df = wbdata.get_dataframe(indicators, country=country2, convert_date=False).to_dict()['GNI per Capita'][arg2]

      if str(df) == 'nan':
        embed = discord.Embed(
            title="Sorry",
              description="**We couldn't find data for that year**",
              color=0xFF5733)

        embed.set_thumbnail(
              url=url
          )
        await ctx.send(embed=embed)

      else:
      

        embed = discord.Embed(
                  title="GNI per capita of {}".format(arg),
                  description=f"The gni per capita of {arg} in {arg2} was/is $`{str(df)}`",
                  color=0xFF5733)
        
        


        result3 = coco.convert(names=arg, to='ISO2')
        
        embed.set_thumbnail(
              url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

        embed.set_footer(text="Information requested by: {}".format(
        ctx.author))

        await ctx.send(embed=embed)
    
    except:
          embed = discord.Embed(
              title="Sorry",
              description="** We could not find data for that year**",
              color=0xFF5733)

          embed.set_thumbnail(
              url=url
          )

          await ctx.send(embed=embed)



  @cog_ext.cog_slash(description='Get the inflation (in %) of a real country in a certain year.')
  async def inflation(self, ctx, country: str, year: int):
    arg = country
    arg2 = str(year)
    try:
      country1 = coco.convert(names=arg, to='iso2')
      country2 = []
      country2.append(country1)
      
      
      
    
      #set up the indicator I want (just build up the dict if you want more than one)
      indicators = {'NY.GDP.DEFL.KD.ZG': 'Inflation (annual %)'}  
      
      #grab indicators above for countires above and load into data frame
      df = wbdata.get_dataframe(indicators, country=country2, convert_date=False).to_dict()['Inflation (annual %)'][arg2]

      if str(df) == 'nan':
        embed = discord.Embed(
            title="Sorry",
              description="**We couldn't find data for that year**".format(
                  arg),
              color=0xFF5733)

        embed.set_thumbnail(
              url=url
          )
        await ctx.send(embed=embed)


      else:
        embed = discord.Embed(
                  title="Inflation of {} in %".format(arg),
                  description=f"The inflation of {arg} in {arg2} was/is `{df}`%",
                  color=0xFF5733)
        
        

      

        result3 = coco.convert(names=arg, to='ISO2')
        
        embed.set_thumbnail(
              url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

        embed.set_footer(text="Information requested by: {}".format(
        ctx.author))

        await ctx.send(embed=embed)

    except:
      embed = discord.Embed(
              title="Sorry",
              description="** We could not find data for that year**",
              color=0xFF5733)

      embed.set_thumbnail(
              url=url
          )

      await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(CountryEconomy2(bot))
  
