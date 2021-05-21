import discord
from discord.ext import commands
import country_converter as coco
import random

from countryinfo import CountryInfo

global quiz_country_list
quiz_country_list = list(CountryInfo().all().keys())

@commands.command()
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


def setup(bot):
  bot.add_command(flag)