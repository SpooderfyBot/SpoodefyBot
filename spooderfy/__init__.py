from .setup.logger import Logger
from .setup import loop

loop.install()
log = Logger.log

from .bot import Spooderfy, run
