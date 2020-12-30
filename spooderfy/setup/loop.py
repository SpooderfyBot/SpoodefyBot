import asyncio
from datetime import datetime


def install():
    try:
        import uvloop
        uvloop.install()
        if __name__ == "__main__":
            now = datetime.now()
            print(
                f"[ {now.strftime('%H:%M:%S | %d %b')} ][ WORKER ]"
                f" Selected uvloop event loop"
            )
    except ImportError:
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        if __name__ == "__main__":
            now = datetime.now()
            print(
                f"[ {now.strftime('%H:%M:%S | %d %b')} ][ WORKER ]"
                f" Selected selector event loop"
            )
