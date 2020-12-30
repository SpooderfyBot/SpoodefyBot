from discord.ext import commands
from discord import Intents

from . import log, Logger


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

    async def on_ready(self):
        """ This is only called if in PRODUCTION = False """
        log("Development bot online! ")

    async def on_shard_ready(self, shard_id):
        """ This is only called if in PRODUCTION = True """
        log(f"Production shard {shard_id} has connected!")


def run(
    token: str,
    shards: tuple,
    total_shards: int,
    cluster_no: int,
    prefix: str,
    **kwargs,
):
    Logger.set_cluster(cluster_no)
    Spooderfy.PRODUCTION = kwargs.pop("production")

    intents = Intents.default()
    intents.members = False
    intents.emojis = False
    intents.integrations = False
    intents.webhooks = False
    intents.invites = False
    intents.voice_states = False
    intents.presences = False
    intents.typing = False
    intents.reactions = True

    bot = Spooderfy(
        prefix,
        shard_ids=list(shards),
        shard_count=total_shards,
        intents=intents,
        **kwargs,
    )

    bot.run(token)