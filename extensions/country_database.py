from discord.ext import commands
import discord
import pycountry, re

@commands.command()
async def list(ctx, arg):

    check = arg
    new_list = []
  
    for x in pycountry.countries:
        s = x.name
        if re.match(check, s, re.I):
            new_list.append(x.name)

    seen = {}
    dupes = []

    for x in new_list:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
                new_list.pop(index(x))
            seen[x] += 1

    
    for i in range(0, len(new_list)):
              new_list[i] = '`' +new_list[i]+ '`'
    result1 = " |".join(new_list)

    result2 = re.sub(r'(?<=[|])(?=[^\s])', r' ', result1)

  

    if not result2:
        embed = discord.Embed(
            title="Sorry",
            description='**there are no countries starting with {}**'.format(
                arg),
            color=0xFF5733)

        embed.set_thumbnail(
            url=
            'https://graduan.sgp1.digitaloceanspaces.com/media/264388/w770/a3d955ec-f826-4041-81d5-e13c040174b4.jpeg'
        )

        await ctx.channel.send(embed=embed)

    else:
        embed = discord.Embed(
            title="Countries starting with " + arg,
            description='**{result2}**'.format(result2=result2),
            color=0xFF5733)

        await ctx.channel.send(embed=embed)


@list.error
async def list_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {db[str(ctx.guild.id)]}list <letter>```')
    await ctx.channel.send(embed=embed)



def setup(bot):
  bot.add_command(list)
