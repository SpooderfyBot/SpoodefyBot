import spooderfy

from os import getenv
from importlib import reload

from scaler import BotScaler


def get_bot(restart: bool):
    """
    Called when a bot instance is made, this can be due to a reload()
    call by the Scaler as well.
    """

    if restart:
        reload(spooderfy)
    else:
        spooderfy.loop.install()

    return getattr(spooderfy, "run")


if __name__ == '__main__':
    runner = BotScaler(
        get_bot=get_bot,
        bot_token=str(getenv("BOT_TOKEN")),
        num_workers=1,
        num_shards=1,
        prefix="sp!",
        production=False,
    )

    runner.start()
    runner.rolling_restart()
    runner.wait_until_finished()