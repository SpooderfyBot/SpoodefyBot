from importlib import import_module

from scaler import BotScaler


def get_bot():
    """
    Called when a bot instance is made, this can be due to a reload()
    call by the Scaler as well.
    """

    bot_module = import_module("spooderfy")
    return getattr(bot_module, "run")


runner = BotScaler(
    get_bot=get_bot,
    num_workers=1,
    num_shards=1,
    prefix="sp!",
    production=False,
)

if __name__ == '__main__':
    runner.start()