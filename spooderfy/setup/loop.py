import asyncio

from . import log


def install():
    try:
        import uvloop
        uvloop.install()
        log("Selected uvloop event loop", runtime=True)
    except ImportError:
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        log("Selected Selector event loop", runtime=True)
