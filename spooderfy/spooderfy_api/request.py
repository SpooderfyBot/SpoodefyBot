
from asyncio import AbstractEventLoop, get_event_loop
from enum import Enum
from typing import Optional

from aiohttp import ClientSession, ClientResponse


BASE_URL = "https://spooderfy.com/api"


class Methods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DEL = "DELETE"


class Requester:
    def __init__(self, loop: Optional[AbstractEventLoop] = None):
        self._loop = loop or get_event_loop()
        self._loop.create_task(self._setup())

        self._session: Optional[ClientSession] = None

    async def _setup(self):
        self._session = ClientSession()

    async def request(
            self,
            method: Methods,
            endpoint: str,
            json: Optional[dict] = None
    ) -> ClientResponse:
        return await self._session.request(method.value, BASE_URL + endpoint, json=json)

