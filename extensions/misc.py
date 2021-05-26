from discord.ext import commands
import discord
import requests, os
import datetime
from replit import db
import time



@commands.command()
async def invite(ctx):
  await ctx.send(embed=discord.Embed(title='Invite link', description='Use this link to invite the bot to your servers: https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands'))





@commands.command()
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
     



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





@commands.command()
async def changelog(ctx):
  embed = discord.Embed(title='Changelog', description='''**1.** Added new `.meme` feature
  **2.** New `.coinflip` feature
  **3.** Added statistics for `work commands issued`
  **4.** Added Statistics for `war` on country profiles
  **5.** Added a special feature only in the support server
  **6.** Added new feature `.gift` (allows you to gift population to other users
  **7.** New autocorrect when you misspell a command
  ''')
  await ctx.send(embed=embed)

@commands.command(name='calc')
async def my_command(ctx, *, arg):
    result = eval(arg)
    await ctx.send(result)

def setup(bot):
  bot.add_command(color)
  bot.add_command(lol)
  bot.add_command(ping)
  bot.add_command(changelog)
  bot.add_command(my_command)
  bot.add_command(invite)