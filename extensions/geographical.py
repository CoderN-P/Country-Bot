import discord
from discord.ext import commands
import country_converter as coco
import random, re
from fuzzywuzzy import fuzz
from mongomethods import get_prefix
from countryinfo import CountryInfo

cc = coco.CountryConverter()

class GeographicalInfo(commands.Cog, name='Geographical Info', description='Commands that give you geographical information about a country'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(description='Check the population of a real country.', brief='Check the population of a real country.')
  async def area(self, ctx, *, country):
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


  @commands.command(description='Check the region that a country is located in. (Must be a real country)', brief='Check the region that a country is located in.')
  async def region(self, ctx, *, country):

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


  @commands.command(description='Check the subregion that a country is located in. (Must be a real country)', brief='Check the subregion that a country is located in.')
  async def subregion(self, ctx, *, country):
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


  @commands.command(description='Get all the bordering countries of a real country.', brief='Get all the bordering countries of a real country.')
  async def borders(self, ctx, *, country):
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


  
  @commands.command(description='Get all the timezones located in a real country.', brief='Get all the timezones located in a real country.')
  async def timezone(self, ctx, *, country):
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


  @commands.command(description='Get the rough coordinates of a real country.', brief='Get the rough coordinates of a real country.')
  async def coords(self, ctx, *, country):
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



def setup(bot):
  bot.add_cog(GeographicalInfo(bot))