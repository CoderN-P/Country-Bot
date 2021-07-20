import discord
from discord.ext import commands
import country_converter as coco
import random
from fuzzywuzzy import fuzz
from mongomethods import get_prefix
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


@commands.command(name='capital')
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
            description="** We could not find data for   {country}**".format(
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
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}capital <country>```')
    await ctx.channel.send(embed=embed)

def setup(bot):
  bot.add_command(flag)
  bot.add_command(cap)