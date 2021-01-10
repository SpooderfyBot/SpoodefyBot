import discord
import os

from traceback import print_exc
from discord.ext import commands

from . import log
from . import error_handler as eh


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

    async def on_shard_ready(self, shard_id):
        """ This is only called if in PRODUCTION = True """
        log(f"Production shard {shard_id} has connected!")

    async def on_command_error(self, ctx: commands.Context, exception):
        exception = getattr(exception, "original", exception)

        if isinstance(exception, commands.CommandNotFound):
            return

        elif isinstance(exception, (discord.Forbidden, commands.BotMissingPermissions)):
            return await eh.missing_permissions(ctx)






