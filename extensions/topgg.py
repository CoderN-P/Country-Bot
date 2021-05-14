from discord.ext import commands
import dbl
class TopGG1(commands.Cog):
    """
    This example uses dblpy's autopost feature to post guild count to top.gg every 30 minutes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgxMDY2MjQwMzIxNzk0ODY3MiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE1NzQwMDA2fQ.eFEgjaUOU4J1WagbKLzFSNgqfEP07-cOmdT3MYKlIFI'  # set this to your DBL token
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