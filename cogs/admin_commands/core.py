from discord.ext import commands
from changeprefix import changeprefix
from configurechannel import configurechannel
from unconfigurechannel import unconfigurechannel


class AdminCommands(
    commands.Cog, name="Admin/Configuration", description="Commands only for admins"
):
    def __init__(self, bot):
        self.bot = bot


setattr(AdminCommands, "changeprefix", changeprefix)
setattr(AdminCommands, "configurechannel", configurechannel)
setattr(AdminCommands, "unconfigurechannel", unconfigurechannel)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
