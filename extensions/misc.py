from discord.ext import commands
import discord
from youtube_search import YoutubeSearch
import requests
from replit import db

@commands.command()
async def youtube_search(ctx, *, query):
  results = YoutubeSearch(query, max_results=10).to_dict()
  vid = results[0]
  
  url = vid['url_suffix']
  embed = discord.Embed(title=query, url=f'https://www.youtube.com{url}')
  

  embed.add_field(name=results[0]['title'], value=f'''**Channel:** {results[0]['channel']} 
  **Views:** {results[0]['views']}
  **Published:** {results[0]['publish_time']}
  **Long description:** {results[0]['long_desc']}
  **Duration:** {results[0]['duration']}''')

  embed.set_thumbnail(url=results[0]['thumbnails'][0])

  await ctx.channel.send(embed=embed)






@youtube_search.error 
async def youtube_search_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
      embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}youtube_search <search query>```')
      await ctx.channel.send(embed=embed)

@commands.command()
async def color(ctx, *, rgb):
  if rgb.startswith("#"):
    info = requests.get(f"https://www.thecolorapi.com/id?hex={rgb[1:]}")
  else:
    info = requests.get(f"https://www.thecolorapi.com/id?rgb={rgb}")

    
  try:
    info = info.json()

    hex1 = info['hex']['value']

    rgb1 = info['rgb']['value'][:-1]
    
    rgb1 = rgb1[4:]
    print(rgb1)

    readableHex = int(hex(int(hex1.replace("#", ""), 16)), 0)


    name = info['name']['value']

    cmyk = info["cmyk"]["value"][5:][:-1]
    cmyk.replace('NaN', '0')

    hsl = info['hsl']['value'][4:][:-1]

    hsl.replace('%', '')

    hsv = info['hsv']['value'][4:][:-1]
    hsv.replace('%', '')

    xyz = info['XYZ']['value'][4:][:-1]
    
    rgb2 = rgb1.split(',')
    rgb2 = [float(i) for i in rgb2]
    
    embed = discord.Embed(title=name, description=None, color=readableHex)

    embed.add_field(name='RGB', value=rgb1, inline=True)
    embed.add_field(name='HEX', value=hex1)

    embed.add_field(name='CMYK', value=cmyk)
    embed.add_field(name='HSL', value=hsl)
    embed.add_field(name='HSV', value=hsv, inline=True)
    embed.add_field(name='XYZ', value=xyz, inline=True)

    

    
    embed.set_image(url=f'https://singlecolorimage.com/get/{hex1[1:]}/400x100.png')
    await ctx.channel.send(embed=embed)

  except:
      embed=discord.Embed(title='Error', description=':x: Invalid Hex or RGB')
      await ctx.channel.send(embed=embed)


@color.error 
async def color_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
      embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}color <rgb or hex>```')
      await ctx.channel.send(embed=embed)




@commands.command()
async def lol(ctx):
   embed = discord.Embed(title='LOL')
   
   embed.set_image(url='https://freepngimg.com/thumb/internet_meme/11-2-lol-face-meme-png.png')
   
  
    
   await ctx.channel.send(embed=embed)









def setup(bot):
  bot.add_command(youtube_search)
  bot.add_command(color)
  bot.add_command(lol)