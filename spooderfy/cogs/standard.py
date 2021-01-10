from discord.ext import commands

from .. import Spooderfy, utils


HELP_DICT = utils.get_help("help")


class GeneralCommands(commands.Cog):
    def __init__(self, bot: Spooderfy):
        self.bot = bot

    @commands.group(aliases=["h"])
    async def help(self, ctx):
        pass


def setup(bot: Spooderfy):
    bot.add_cog(GeneralCommands(bot))