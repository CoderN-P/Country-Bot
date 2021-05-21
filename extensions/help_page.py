import discord
from discord.ext import commands
from replit import db
import asyncio


main_url = 'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'

geographical = discord.Embed(title=":map: 1/10  Geographical info", description='''`area`, `borders`,`coords`, `region`, `subregion`, `timezone`''', color=0xFF5733)

geographical.set_thumbnail(
            url= main_url
            
        )

general = discord.Embed(title=":information_source:  3/10 General info", description="`capital`, `population`, `states`, `language`, `covid`, `stats`, `flag`, `changelog`, `meme`", color=0xFF5733)

general.set_thumbnail(
            url= main_url
            
        )

economy = discord.Embed(title=":moneybag: 2/10  Economy", description="`currency`, `gni_percap`, `gdp_percap`, `inflation`", color=0xFF5733)

economy.set_thumbnail(
            url= main_url
            
        )

country_database = discord.Embed(title=':scroll: 4/10  Country Database', description='`list`', color=0xFF5733)

country_database.set_thumbnail(
            url= main_url
            
        )

admin_stuff = discord.Embed(title=':lock: 5/10 Needs admin permissions', description='`changeprefix`', color=0xFF5733)

admin_stuff.set_thumbnail(
            url= main_url
            
        )

games = discord.Embed(title=':video_game: 6/10 Games', description='`guess_capital`, `work`, `start`, `store`, `profile`, `daily`, `change`, `quit`, `war`, `gift`, `tax`', color=0xFF5733)

gambling = discord.Embed(title=':game_die: 8/10 Gambling', description='`coinflip`', color=0xFF5733)

misc = discord.Embed(title=':file_folder: 7/10 Misc', description='`color`, `ping`, `lol`', color=0xFF5733)

meme_commands = discord.Embed(title='🤣 9/10 Meme Commands/Animals', description='`dog`, `meme`, `cat`, `snake`, `aww`', color=0xFF5733)
developer_commands = discord.Embed(title=':tools: 10/10 Developer Commands', description='`eval`, `stop_drops`', color=0xFF5733)

games.set_thumbnail(
            url= main_url
            
        )







class HelpCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx, *arg):
      prefix = db[str(ctx.guild.id)]
      if len(arg) == 0:
          main = discord.Embed(title="Country Bot Help",
                                description=f'''**Prefix = `{prefix}`
        
            Type `{prefix}help <command>` for more information on a specific  command. (HIGHLY RECOMMENDED)
            
            Forgot the bot's prefix?
            Don't worry type **<@!810662403217948672> prefix** and Country Bot will tell you its prefix for this server**

            **Links: [vote (top.gg)](https://top.gg/bot/810662403217948672/vote) | [invite](https://discord.com/api/oauth2/authorize?client_id=810662403217948672&permissions=2048&scope=bot%20applications.commands) | [top.gg](https://top.gg/bot/810662403217948672#/) | [support server](https://discord.gg/hCgh9wngkS) | [discordbotlist](https://discord.ly/country-bot)**
            
            Tip: Use `{db[ctx.guild.id]}war @Player` to wage war on your friends countries!!

            Tip2: Use `{db[ctx.guild.id]}daily` to receive 100 population every day!

            **Check out `.changelog` to see new features that have come out!!!**

            Use the `{db[ctx.guild.id]}configurechannel <channel>` and `{db[ctx.guild.id]}unconfigurechannel <channel>` command to receive updates about the bot in that channel



        ''', color=0xFF5733)

          main.set_thumbnail(
              url= main_url
              
          )

          
          message = await ctx.channel.send(embed=main)
                              

            

          contents = [main, geographical, economy, general, country_database, admin_stuff, games, misc, gambling, meme_commands, developer_commands]

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
          if arg == 'area':
              embed = discord.Embed(title="Area",
                                    description=f'''**Usage: `{prefix}area <country>`
          Returns the area of the country in `sq. km`**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url= main_url
                  
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'capital':
              embed = discord.Embed(title="Capital",
                                    description='''**Usage: `.capital <country>`
          Returns the capital city of the country**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'currency':
              embed = discord.Embed(title="Currency",
                                    description=f'''**Usage: `{prefix}currency <country>`
          Returns the currency(s) used by the country**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'population':
              embed = discord.Embed(
                  title="Population",
                  description=f'''**Usage: `{prefix}population <country>`
          Returns the approximate population of the country**''',
                  color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'states':
              embed = discord.Embed(title="States/Provinces",
                                    description=f'''**Usage: `{prefix}states <country>`
          Returns the states/provinces in the country**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)
          elif arg == 'language':
              embed = discord.Embed(title="Language",
                                    description=f'''**Usage: `{prefix}language <country>`
          Returns the language(s) of the country**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )
              await ctx.channel.send(embed=embed)

          elif arg == 'region':
              embed = discord.Embed(title="Region",
                                    description=f'''**Usage: `{prefix}region <country>`
          Returns the general region the country is located in**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )
              await ctx.channel.send(embed=embed)

          elif arg == 'subregion':
              embed = discord.Embed(
                  title="Subregion",
                  description=f'''**Usage: `{prefix}subregion <country>`
          Returns the subregion the country is located in**''',
                  color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )
              await ctx.channel.send(embed=embed)

          elif arg == 'timezone':
              embed = discord.Embed(title="Timezone",
                                    description=f'''**Usage: `{prefix}timezone <country>`
          Returns the timezone(s) located in the country**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )
              await ctx.channel.send(embed=embed)

          elif arg == 'borders':
              embed = discord.Embed(title="Borders",
                                    description=f'''**Usage: `{prefix}borders <country>`
          Returns the countries that border the selected country**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )
              await ctx.channel.send(embed=embed)

          elif arg == 'coords':
              embed = discord.Embed(title="Coords",
                                    description=f'''**Usage: `{prefix}coords <country>`
          Returns the coordinates of the country. 
          A negative coordinate means south or west. 
          A positive coordinate means North or East.
          Longitude shows location horizontally
          Latitude shows location vertically
          Format: `Longitude, Latitude`**''',
                                    color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )
              await ctx.channel.send(embed=embed)

          elif arg == 'list':
              embed = discord.Embed(
                  title="Borders",
                  description=f'''**Usage: `{prefix}list <letter or letters>`
          Returns the countries that start with the selected letter or letters**''',
                  color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )
              await ctx.channel.send(embed=embed)

          elif arg == 'gdp_percap':
              embed = discord.Embed(
                  title="gdp_percap",
                  description=f'''**Usage: `{prefix}gdp_percap <country> <year>`
          Returns the GDP per capita of the country in that year**''',
                  color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'gni_percap':
              embed = discord.Embed(
                  title="gni_percap",
                  description=f'''**Usage: `{prefix}gni_percap <country> <year>`
          Returns the GNI per capita of the country in that year**''',
                  color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'inflation':
              embed = discord.Embed(
                  title="Inflation",
                  description=f'''**Usage: `{prefix}inflation <country> <year>`
          Returns the percent of inflation of the country in that year.**''',
                  color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'covid':
              embed = discord.Embed(
                  title="Covid 19 info",
                  description=f'''**Usage: `{prefix}covid <country>`
          Returns information about the coronavirus for the country**''',
                  color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed = embed)
              
          elif arg == 'changeprefix':
            embed = discord.Embed(
                  title="Change prefix",
                  description=f'''**Usage: `{prefix}changeprefix <prefix>`
          Sets a new prefix. User needs to have admin to use this command.**''',
                  color=0xFF5733)
            embed.set_thumbnail(
                  url=
                  main_url
              )

            await ctx.channel.send(embed = embed)

          elif arg == 'guess_capital':
              embed = discord.Embed(
                  title="Guess the Capital",
                  description=None,
                  color=0xFF5733)
          
              embed.add_field(name = "Usage", value = f''' ```{prefix}guess_capital``` ***OR***```{prefix}guess_capital reverse```''', inline = False)

              embed.add_field(name = "Normal mode", value = '''A random country is given. Players will try to give the capital before the time rns out.''')

              embed.add_field(name="Reverse mode", value='''A capital city of a country is given. Players will try to give the country before the time runs out.''')

              embed.add_field(name="Things to Note", value='''Time limit must not exceed `300` seconds.
              Type `quit` while playing to quit the game. 
              Have Fun!!! 🤞''')
              
              

              embed.set_thumbnail(
                      url=
                      main_url
                  )

              await ctx.channel.send(embed = embed)

          elif arg == 'work':
            embed=discord.Embed(title='Work', description=f'''**Usage: `{prefix}work`
            You worked for your country and got more people to live in it. Has a cooldown of 15 sec**''', color=Color.teal())

            
          
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)
          
          elif arg == 'flag':
            embed=discord.Embed(title='Flag', description=f'''**Usage: `{prefix}flag`
                            OR         `{prefix}flag <country>`
            Returns a flag of a random country**''', color=Color.teal())

            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)
          
          elif arg == 'store':
            embed=discord.Embed(title='Store', description=f'''**Usage: `{prefix}store`
            The store where you can buy upgrades for your country!**''', color=Color.teal())

            
          
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)
          
          elif arg == 'profile':
            embed=discord.Embed(title='Profile', description=f'''**Usage: `{prefix}profile`
            View stats about your country**''', color=Color.teal())

            
          
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)
          
          elif arg == 'start':
            embed=discord.Embed(title='Start', description=f'''**Usage: `{prefix}start`
              Start your country**''', color=Color.teal())

              
            
            embed.set_thumbnail(
                      url=
                      main_url
                  )
              
            await ctx.channel.send(embed=embed)

          

          elif arg == 'stats':
              embed = discord.Embed(title="Stats",
                                    description=f'''**Usage: `{prefix}stats`
          Returns general information about the bot such as, `latency`, `server count`, and `memory usage`**''', color=0xFF5733)
              embed.set_thumbnail(
                  url=
                  main_url
              )

              await ctx.channel.send(embed=embed)

          elif arg == 'quit':
            embed=discord.Embed(title='Quit', description=f'''**Usage: `{prefix}quit`
            You can use this command to quit your country.**''', color=Color.teal())

            
          
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)

          elif arg == 'change':
            embed=discord.Embed(title='Change', description=f'''**Usage: `{prefix}change <name>`
            Change your country name**''', color=Color.teal())

            
          
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)

          
          elif arg == 'buy':
            embed=discord.Embed(title='Buy', description=f'''**Usage: `{prefix}buy <ID> <amount>`
            Amount is only specified when buying multiplier boosts
            Buy uogrades for your country**''', color=Color.teal())

            
          
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)

          elif arg == 'daily':
            embed=discord.Embed(title='Daily', description=f'''**Usage: `{prefix}daily`
            Get 100 more people into your country every day. Has a 24 hour cooldown**''', color=Color.teal())

            
          
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)

      

          elif arg == 'color':
            embed=discord.Embed(title='Color', description=f'''**Usage: `{prefix}color <rgb or hex>`
            Returns information about the color you entered**''', color=Color.teal())
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)
          elif arg == 'war':
            embed=discord.Embed(title='War', description=f'''**Usage: `{prefix}war <user>`
            Wage war on another user**''', color=Color.teal())
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)
          elif arg == 'gift':
            embed=discord.Embed(title='Gift', description=f'''**Usage: `{prefix}gift <user> <amount>`
            Allows you to gift population to another user**''', color=Color.teal())
            embed.set_thumbnail(
                    url=
                    main_url
                )
            
            await ctx.channel.send(embed=embed)


          elif arg == 'coinflip':
            embed=discord.Embed(title='Coinflip', description=f''' [] = Optional <> = Mandatory
            **Usage: `{prefix}coinflip <heads | tails> [bet amount]`
            
            Allows you to gamble with your population.**''', color=Color.teal())
            embed.set_thumbnail(
                    url=
                    main_url
                )

            await ctx.channel.send(embed=embed)

          elif arg.lower() == 'changelog':
            embed=discord.Embed(title='Coinflip', description=f''' 
            **Usage: `{prefix}changelog`
            
          Shows the recent changes to the bot.**''', color=Color.teal())
            embed.set_thumbnail(
                    url=
                    main_url
                )

          elif arg.lower() == 'tax':
            embed = discord.Embed(title='Tax', description='''**Usage:** `.tax`
            tax your population to earn coins''', color=Color.teal())
            
            embed.set_thumbnail(
                    url=
                    main_url
                )

            await ctx.send(embed=embed)
            
            



        
          
          else:
              embed = discord.Embed(title="Country Bot Help",
                                    description=f'''**Prefix = `{db[ctx.guild.id]}`

          ```diff\n- Woops!, the command "{arg}" doesn't exist  
          ```
        
            Type `{db[ctx.guild.id]}help <command>` for more information on a specific  command.**
            
            '''.format(arg=arg),
                                    color=0xFF5733)

              embed.set_thumbnail(
                url=
                  main_url
              )

              await ctx.channel.send(embed=embed)


def setup(bot):
  bot.add_cog(HelpCog(bot))