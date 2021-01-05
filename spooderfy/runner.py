from discord import Intents

from . import Logger, loop, Spooderfy


def run(
    shutdown,
    token: str,
    shards: tuple,
    total_shards: int,
    cluster_no: int,
    prefix: str,
    **kwargs,
):
    # Set logger cluster no
    Logger.CLUSTER_ID = cluster_no

    # Determines if we need to use sharded readies
    Spooderfy.PRODUCTION = kwargs.pop("production")

    # Install custom loop if installed
    loop.install()

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
    bot.loop.create_task(bot.watch_shutdown(shutdown))
    bot.run(token)