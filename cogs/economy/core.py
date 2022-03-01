from currency import currency
from discord.ext import commands

class CountryEconomy(
    commands.Cog,
    name="Economy Data",
    description="Commands that give you data about a country's economy.",
):
    def __init__(self, bot):
        self.bot = bot

setattr(CountryEconomy, 'currency', currency)

def setup(bot):
    bot.add_cog(CountryEconomy(bot))