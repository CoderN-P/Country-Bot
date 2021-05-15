from discord.ext import commands
import dbl, os
class TopGG1(commands.Cog):
    """
    This example uses dblpy's autopost feature to post guild count to top.gg every 30 minutes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ['TOPGGTOKEN'] # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)  # Autopost will post your guild count every 30 minutes

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print("Received an upvote:", data)

    
    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print("TEST VOTE")
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print("Received a test upvote:", "\n", data, sep="")


def setup(bot):
  bot.add_cog(TopGG1(bot))