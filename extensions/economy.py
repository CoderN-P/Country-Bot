import discord
from discord.ext import commands
import country_converter as coco
from countryinfo import CountryInfo
import wbdata, pycountry, re

cc = coco.CountryConverter()

@commands.command()
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

@currency.error
async def currency_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}currency <country>```')
    await ctx.channel.send(embed=embed)


@commands.command()
async def gdp_percap(ctx, arg, arg2):
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
            url=
           'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )
      await ctx.channel.send(embed=embed)
    else:
      embed = discord.Embed(
                title="GDP per capita of {}".format(arg),
                description=f'The gdp per capita of {arg} in {arg2} is/was $`{df}`',
                color=0xFF5733)
      
      


      result3 = coco.convert(names=arg, to='ISO2')
      embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

      embed.set_footer(text="Information requested by: {}".format(
      ctx.message.author))

      await ctx.channel.send(embed=embed)

  except:
      embed = discord.Embed(
          title="Sorry",
            description="**We couldn't find data for that year**",
            color=0xFF5733)

      embed.set_thumbnail(
            url=
           'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

      await ctx.channel.send(embed=embed)



@gdp_percap.error
async def gdp_percap_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}gdp_percap <country> <year>```')
    await ctx.channel.send(embed=embed)







@commands.command()
async def gni_percap(ctx, arg, arg2):
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
            url=
           'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )
      await ctx.channel.send(embed=embed)

    else:
    

      embed = discord.Embed(
                title="GNI per capita of {}".format(arg),
                description=f"The gni per capita of {arg} in {arg2} was/is $`{str(df)}`",
                color=0xFF5733)
      
      


      result3 = coco.convert(names=arg, to='ISO2')
      
      embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

      embed.set_footer(text="Information requested by: {}".format(
      ctx.message.author))

      await ctx.channel.send(embed=embed)
  
  except:
        embed = discord.Embed(
            title="Sorry",
            description="**We could not find data for that year",
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg')
        

        await ctx.channel.send(embed=embed)

@gni_percap.error
async def gni_percap_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}gni_percap <country> <year>```')
    await ctx.channel.send(embed=embed)








@commands.command()
async def inflation(ctx, arg, arg2):

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
            url=
           'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )
      await ctx.channel.send(embed=embed)


    else:
      embed = discord.Embed(
                title="Inflation of {} in %".format(arg),
                description=f"The inflation of {arg} in {arg2} was/is `{df}`%",
                color=0xFF5733)
      
      

    

      result3 = coco.convert(names=arg, to='ISO2')
      
      embed.set_thumbnail(
            url=f'https://flagcdn.com/w80/{result3.lower()}.jpg')

      embed.set_footer(text="Information requested by: {}".format(
      ctx.message.author))

      await ctx.channel.send(embed=embed)

  except:
    embed = discord.Embed(
    title="Sorry",
    description="**We could not find data for that year**",
            color=0xFF5733)

    embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg')

    await ctx.channel.send(embed=embed)


@inflation.error
async def inflation_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}inflation <country> <year>```')
    await ctx.channel.send(embed=embed)






def setup(bot):
  bot.add_command(currency)
  bot.add_command(gdp_percap)
  bot.add_command(inflation)
  bot.add_command(gni_percap)
