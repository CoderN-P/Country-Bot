from discord.ext import commands

from country_list import country_list


class CountryDatabase(
    commands.Cog,
    name="Country Database",
    description="Commands that allow you to find countries!",
):
    def __init__(self, bot):
        self.bot = bot


setattr(CountryDatabase, "country_list", country_list)


def setup(bot):
    bot.add_cog(CountryDatabase(bot))
