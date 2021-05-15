import discord
import requests
from discord.ext import commands

@commands.command()
async def meme(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/wholesomememes').json()
  meme = data
  channel_nsfw = ctx.message.channel.is_nsfw()
  title = meme['title']
  
  if meme['nsfw'] == 'True':
    if channel_nsfw:
      embed = discord.Embed(title=f'{title} [NSFW]', url=meme['postLink'])
      embed.set_image(url=meme['url'])
      author = meme['author']
      likes = meme['ups']
      embed.set_footer(text=f'Author: {author} | 👍 {likes}')
      await ctx.send(embed=embed)

    else:
      embed = discord.Embed(title='Hey!', description=':x: This meme is NSFW!!! You can only see it in an NSFW channel.')
      await ctx.send(embed=embed)

    

  else:
    embed = discord.Embed(title=meme['title'], url=meme['postLink'])
    embed.set_image(url=meme['url'])
    author = meme['author']
    likes = meme['ups']
    embed.set_footer(text=f'Author: {author} | 👍 {likes}')
    await ctx.send(embed=embed)



@commands.command()
async def cat(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/cats').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)



@commands.command()
async def dog(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/dog').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)


@commands.command()
async def aww(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/awww').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)


@commands.command()
async def snake(ctx):
  data = requests.get('https://meme-api.herokuapp.com/gimme/snakes').json()
  meme = data

  
  
  title = meme['title']
  
  
    
  embed = discord.Embed(title=f'{title}', url=meme['postLink'])
  embed.set_image(url=meme['url'])
  author = meme['author']
  likes = meme['ups']
  embed.set_footer(text=f'Author: {author} | 👍 {likes}')
  await ctx.send(embed=embed)


def setup(bot):
  bot.add_command(meme)
  bot.add_command(cat)
  bot.add_command(dog)
  bot.add_command(snake)
  bot.add_command(aww)