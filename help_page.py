import discord
from discord.ext import commands

main_url = 'https://www.bergerpaints.com/imaginecolours/wp-content/uploads/2016/09/flags-of-the-world-1170x693.png'

geographical = discord.Embed(title=":map: 1/9  Geographical info", description='''`area`, `borders`,`coords`, `region`, `subregion`, `timezone`''', color=0xFF5733)

geographical.set_thumbnail(
            url= main_url
            
        )

general = discord.Embed(title=":information_source:  3/9 General info", description="`capital`, `population`, `states`, `language`, `covid`, `stats`, `flag`, `changelog`, `meme`", color=0xFF5733)

general.set_thumbnail(
            url= main_url
            
        )

economy = discord.Embed(title=":moneybag: 2/9  Economy", description="`currency`, `gni_percap`, `gdp_percap`, `inflation`", color=0xFF5733)

economy.set_thumbnail(
            url= main_url
            
        )

country_database = discord.Embed(title=':scroll: 4/9  Country Database', description='`list`', color=0xFF5733)

country_database.set_thumbnail(
            url= main_url
            
        )

admin_stuff = discord.Embed(title=':lock: 5/9 Needs admin permissions', description='`changeprefix`', color=0xFF5733)

admin_stuff.set_thumbnail(
            url= main_url
            
        )

games = discord.Embed(title=':video_game: 6/9 Games', description='`guess_capital`, `work`, `start`, `store`, `profile`, `daily`, `change`, `quit`, `war`, `gift`, `tax`', color=0xFF5733)

gambling = discord.Embed(title=':game_die: 8/9 Gambling', description='`coinflip`', color=0xFF5733)

misc = discord.Embed(title=':file_folder: 7/9 Misc', description='`color`, `youtube_search`, `ping`, `lol`', color=0xFF5733)

developer_commands = discord.Embed(title=':tools: 9/9 Developer Commands', description='`eval`, `stop_drops`', color=0xFF5733)

games.set_thumbnail(
            url= main_url
            
        )








