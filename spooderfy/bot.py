import discord
import os
import re
import typing as t

from traceback import print_exc
from discord.ext import commands

from . import log
from .custom import prefix
from .spooderfy_api import Room


def watch_shutdown(shutdown):
    """ This will return when teh master process signals for us to shutdown """
    shutdown.get()


class Spooderfy(commands.AutoShardedBot):
    PRODUCTION = False

    def __new__(cls, *args, **kwargs):
        if cls.PRODUCTION:
            delattr(cls, "on_ready")
        else:
            delattr(cls, "on_shard_ready")

        instance = super(Spooderfy, cls).__new__(cls)
        return instance

    def __init__(self, command_prefix, **options):
        self.prefix = command_prefix
        self.mentions: t.Optional[set] = None

        self.colour = 0x0DEDE8
        self.site_url = "https://spooderfy.com"
        self.white_icon = "https://cdn.discordapp.com/emojis/773609763015360582.png?v=1"

        self._ready_once = False

        self.rooms: t.Dict[int, Room] = {}

        super().__init__("", **options)

        self.remove_command("help")
        self._load_all_extensions()

    def _load_all_extensions(self):
        for file in os.listdir("./spooderfy/cogs"):
            if file.endswith(".py") and not file.startswith("__"):
                self._load_ext(file[:-3])

    def _load_ext(self, file):
        try:
            self.load_extension(f"spooderfy.cogs.{file}")
            log(f"[ EXTENSION LOADED ] {file}")
        except commands.ExtensionFailed:
            print_exc()
            log(f"[ EXTENSION ERROR ] Extension {file} could not be loaded.")
        except commands.ExtensionNotFound:
            log(f"[ EXTENSION ERROR ] Extension {file} is not found.")

    async def watch_shutdown(self, shutdown):
        await self.loop.run_in_executor(None, watch_shutdown, shutdown)
        await self.logout()

    async def on_ready(self):
        """ This is only called if in PRODUCTION = False """
        log("Development bot online!")

        if not self._ready_once:
            await self.on_ready_once()
            self._ready_once = True

    async def on_shard_ready(self, shard_id):
        """ This is only called if in PRODUCTION = True """
        log(f"Production shard {shard_id} has connected!")

        if not self._ready_once:
            await self.on_ready_once()
            self._ready_once = True

    async def on_ready_once(self):
        self.mentions = prefix.get_mentions(self.user.id)

    async def get_prefix(self, message):
        return (await prefix.acquire_prefix(message.guild)) or self.prefix

    async def on_message(self, message):
        if message.author.bot or not self.is_ready():
            return

        if message.content in self.mentions:
            prefix_ = (await prefix.acquire_prefix(message.guild)) or self.prefix
            return await message.reply(
                "<:spooderfy:773609763015360582> "
                f"**My prefix is `{prefix_}`**"
            )

        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, exception):
        if getattr(ctx, 'handled', False):
            return

        exception = getattr(exception, "original", exception)

        if isinstance(exception, commands.CommandNotFound):
            return

        raise exception






