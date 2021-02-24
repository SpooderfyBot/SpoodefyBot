import discord
from discord.ext import commands

from .. import Spooderfy
from .. import spooderfy_api


class RoomCommands(commands.Cog):
    def __init__(self, bot: Spooderfy):
        self.bot = bot



def setup(bot: Spooderfy):
    bot.add_cog(RoomCommands(bot))