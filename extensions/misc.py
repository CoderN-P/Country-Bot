from discord.ext import commands
import discord
import requests
import os
import datetime
import time
import random
import json
import ast

class Misc(commands.Cog, description='Miscellaneous commands'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='cat-fact', description='Learn some cool cat facts!', brief='Learn some cool cat facts!')
  async def catfact(self, ctx):
    r = requests.get('https://catfact.ninja/fact?max_length=140')
    r = r.json()['fact']
    embed = discord.Embed(title='Cat Fact', description=r)
    await ctx.send(embed=embed)


  @commands.command(name='dog-fact', description='Learn some cool dog facts!', brief='Learn some cool dog facts!')
  async def dogfact(self, ctx):
    r = requests.get('http://dog-api.kinduff.com/api/facts?number=1')
    r = r.json()['facts'][0]
    embed = discord.Embed(title='Dog Fact', description=r)
    await ctx.send(embed=embed)



  @commands.command(description="Get Country Bot's invite link", brief="Get Country Bot's invite link")
  async def invite(self, ctx):
    await ctx.send(embed=discord.Embed(title='Invite link', description='Use this link to invite the bot to your servers: https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands'))

  @commands.command(description='bruh', brief='bruh')
  async def bruh(self, ctx):
    embed = discord.Embed(title='bruh')
    embed.set_image(url='https://media1.tenor.com/images/8daeb547b121eef5f34e7d4e0b88ea35/tenor.gif?itemid=5156041')
    await ctx.send(embed=embed)


  @commands.command(description='Get a random joke, or specify a type of joke: `knock-knock`, `general`, or `programming`', brief='Get a random joke, or specify a type of joke: `knock-knock`, `general`, or `programming`')
  async def joke(self, ctx, *type):
    arg = type
    def jokes(f):
      data = requests.get(f)
      tt = json.loads(data.text)
      return tt
    error_embed = discord.Embed(title='Error', description=':x: That is not a valid option! The valid options are, `knock-knock` `general` and `programming`')
    if len(arg) > 1:
      if ' '.join(arg) == 'knock knock':
        f = f"https://official-joke-api.appspot.com/jokes/knock-knock/random"
        a = jokes(f)

      

        for i in (a):
          await ctx.channel.send(embed=discord.Embed(title=i["setup"], description=i['punchline']))
      else:
        await ctx.send(embed=error_embed)
    elif len(arg) == 1:
      arg = arg[0] 
      if arg not in ['knock-knock', 'general', 'programming']:
        await ctx.send(embed=error_embed)
        return
      f = f"https://official-joke-api.appspot.com/jokes/{arg}/random"
      a = jokes(f)

      

      for i in (a):
        await ctx.channel.send(embed=discord.Embed(title=i["setup"], description=i['punchline']))

    else:
      joke = random.choice(['knock-knock', 'general', 'programming'])

      f = f"https://official-joke-api.appspot.com/jokes/{joke}/random"
      a = jokes(f)

      

      for i in (a):
        embed = discord.Embed(title=i["setup"], description=i['punchline'])
        embed.set_footer(text=f'This was a {joke} joke')
        await ctx.channel.send(embed=embed)

      

  @commands.command(description='Vote for Country Bot to get some cool rewards!', brief='Vote for Country Bot to get some cool rewards!')
  async def vote(self, ctx):
    embed = discord.Embed(title='Vote For Country Bot :)', description='You can vote for country bot [here](https://top.gg/bot/810662403217948672/vote)').set_image(url='https://top.gg/images/dblnew.png').set_footer(text='You can vote every 12 hours')
    await ctx.send(embed=embed)

  @commands.command(description='Get the message ping of the bot.', brief='Get the message ping of the bot.')
  async def ping(self, ctx):
      """ Pong! """
      before = time.monotonic()
      message = await ctx.send("Pong!")
      ping = (time.monotonic() - before) * 1000
      await message.edit(content=f"Pong!  `{int(ping)}ms`")
      
  @commands.command(description='N o t h i n g', brief='N o t h i n g')
  async def nothing(self, ctx):
    await ctx.send('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    


  @commands.command(description='Get information about a color by supplying its rgb/hex', brief='Get information about a color by supplying its rgb/hex')
  async def color(self, ctx, *, rgb_or_hex):
    rgb = rgb_or_hex
    if rgb.startswith("#"):
      info = requests.get(f"https://www.thecolorapi.com/id?hex={rgb[1:]}")
    else:
      info = requests.get(f"https://www.thecolorapi.com/id?rgb={rgb}")

      
    try:
      info = info.json()

      hex1 = info['hex']['value']

      rgb1 = info['rgb']['value'][:-1]
      
      rgb1 = rgb1[4:]
     

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





  @commands.command(description='lol', brief='lol')
  async def lol(self, ctx):
    embed = discord.Embed(title='LOL')
    
    embed.set_image(url='https://freepngimg.com/thumb/internet_meme/11-2-lol-face-meme-png.png')
    
    
      
    await ctx.channel.send(embed=embed)





  @commands.command(description='Country Bot changelog.', brief='Country Bot changelog.')
  async def changelog(self, ctx):
    embed = discord.Embed(title='Changelog', description='''**1.** Added new `.meme` feature
    **2.** New `.coinflip` feature
    **3.** Added statistics for `work commands issued`
    **4.** Added Statistics for `war` on country profiles
    **5.** Added a special feature only in the support server
    **6.** Added new feature `.gift` (allows you to gift population to other users
    **7.** New autocorrect when you misspell a command
    ''')
    await ctx.send(embed=embed)

  @commands.command(name='calc', description='Calculate a mathematical expression, (no variables allowed)', brief='Calculate stuff')
  async def my_command(self, ctx, *, arg):
      result = ast.literal_eval(arg)
      await ctx.send(result)

  @commands.command(description='Country Bot will reverse the text you give him.', brief='Country Bot will reverse the text you give him.')
  async def backwards(self, ctx, *, text):

    await ctx.send(text[::-1].strip('@'))

def setup(bot):
  bot.add_cog(Misc(bot))
