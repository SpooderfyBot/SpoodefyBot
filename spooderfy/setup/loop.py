import asyncio


def install():
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
