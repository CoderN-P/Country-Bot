import discord
from discord.ext import commands
from mongomethods import get_prefix
import asyncio
import json
from discord import Color

main_url = 'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'

geographical = discord.Embed(title=":map: 1/11  Geographical info", description='''`area`, `borders`,`coords`, `region`, `subregion`, `timezone`''', color=0xFF5733)

geographical.set_thumbnail(
            url= main_url
            
        )

general = discord.Embed(title=":information_source:  3/11 General info", description="`capital`, `population`, `states`, `language`, `covid`, `stats`, `flag`, `changelog`, `meme`", color=0xFF5733)

general.set_thumbnail(
            url= main_url
            
        )

economy = discord.Embed(title=":moneybag: 2/11  Economy", description="`currency`, `gni_percap`, `gdp_percap`, `inflation`", color=0xFF5733)

economy.set_thumbnail(
            url= main_url
            
        )


configuration = discord.Embed(title=":gear: 11/11 Configuration", description="`configurechannel`, `unconfigurechannel`", color=0xFF5733)

configuration.set_thumbnail(
            url= main_url
            
        )

country_database = discord.Embed(title=':scroll: 4/11  Country Database', description='`list`', color=0xFF5733)

country_database.set_thumbnail(
            url= main_url
            
        )

admin_stuff = discord.Embed(title=':lock: 5/11 Needs admin permissions', description='`changeprefix`', color=0xFF5733)

admin_stuff.set_thumbnail(
            url= main_url
            
        )

games = discord.Embed(title=':video_game: 6/11 Games', description='`guess_capital`, `work`, `start`, `store`, `profile`, `daily`, `change`, `quit`, `war`, `gift`, `tax`', color=0xFF5733)

gambling = discord.Embed(title=':game_die: 8/11 Gambling', description='`coinflip`, `dice`', color=0xFF5733)

misc = discord.Embed(title=':file_folder: 7/11 Misc', description='`color`, `ping`, `lol`', color=0xFF5733)

meme_commands = discord.Embed(title='🤣 9/11 Meme Commands/Animals', description='`dog`, `meme`, `cat`, `snake`, `aww`', color=0xFF5733)
developer_commands = discord.Embed(title=':tools: 10/11 Developer Commands', description='`eval`, `stop_drops`', color=0xFF5733)

games.set_thumbnail(
            url= main_url
            
        )







class HelpCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx, *arg):
      prefix = await get_prefix(ctx.guild.id)
      if len(arg) == 0:
          
          main = discord.Embed(title="Country Bot Help",
                                description=f'''**Prefix = `{prefix}`
        
            Type `{prefix}help <command>` for more information on a specific  command. (HIGHLY RECOMMENDED)
            
            Forgot the bot's prefix?
            Don't worry type **<@!810662403217948672> prefix** and Country Bot will tell you its prefix for this server**

            __Country Bot Partners!__
            [**Check out TestPreparer today!**](https://testpreparer.gq)

            **Links: [vote (top.gg)](https://top.gg/bot/810662403217948672/vote) | [invite](https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands) | [top.gg](https://top.gg/bot/810662403217948672#/) | [discordbotlist](https://discord.ly/country-bot)** | [Github Repo](https://github.com/Codern-P/Country-Bot)



        ''', color=0xFF5733)

          main.add_field(name='Tips', value=
        f'''1. Use `{prefix}war @Player` to wage war on your friends countries!!

            2. Use `{prefix}daily` to receive 100 population every day!''')



          main.add_field(name='More Tips', value=f'''3. **Check out `.changelog` to see new features that have come out!!!**''')

          main.add_field(name='Need additional help!', value='Join the [support server](https://discord.gg/hCgh9wngkS)')

          

          main.set_thumbnail(
              url= main_url
              
          )

          
          message = await ctx.channel.send(embed=main)
                              
    
            

          contents = [main, geographical, economy, general, country_database, admin_stuff, games, misc, gambling, meme_commands, developer_commands, configuration]

          

          pages = len(contents)
          cur_page = 1

          await message.add_reaction("⏪")
          await message.add_reaction("◀️")
          await message.add_reaction("▶️")
          await message.add_reaction("⏩")
          await message.add_reaction("❌")

          def check2(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "⏩", "⏪", "❌"] and reaction.message == message

          



          
          while True:
            try:
              reaction, user = await self.bot.wait_for("reaction_add", timeout=100, check=check2)

              

            
              
              if str(reaction.emoji) == "▶️" and cur_page < pages:
                  cur_page += 1
                  
                  await message.edit(embed=contents[cur_page-1])
                  

              elif str(reaction.emoji) == "◀️" and cur_page > 1:
                  cur_page -= 1
                  
                  await message.edit(embed=contents[cur_page-1])
                  

              elif str(reaction.emoji) == "⏩":
                cur_page = pages
                
                await message.edit(embed=contents[cur_page-1])
                
              
              elif str(reaction.emoji) == "⏪":
                cur_page = 1
                await message.edit(embed=contents[0])
                
              
              elif str(reaction.emoji) == "❌":
                await message.delete()
                break
              
            except asyncio.TimeoutError:
              await message.delete()
              break

          
        

          

          

        

          

          


          

          
      if len(arg) == 1:
          arg = ' '.join(arg)
          file = json.load(open('help_page1.json'))
          
          if arg.lower() in file.keys():
            command = file[arg]
            embed = discord.Embed(title=command[0], description=command[1])
            await ctx.send(embed=embed)
           

          
          else:

              embed = discord.Embed(title="Country Bot Help",
                                    description=f'''**Prefix = `{prefix}`

          ```diff\n- Woops!, the command "{arg}" doesn't exist  
          ```
        
            Type `{prefix}help <command>` for more information on a specific  command.**
            
            '''.format(arg=arg),
                                    color=0xFF5733)

              embed.set_thumbnail(
                url=
                  main_url
              )

              await ctx.channel.send(embed=embed)
@commands.command(name='update-help')
@commands.is_owner()
async def update_help(ctx, item, arg, arg2):
  file = json.load(open("help_page1.json"))
  file[item] = [arg, arg2]
  with open("help_page1.json", "w") as f:
    f.write(json.dumps(file))
  await ctx.send(embed=discord.Embed(title=file[item][0], description=file[item][1]))

def setup(bot):
  bot.add_cog(HelpCog(bot))
  bot.add_command(update_help)