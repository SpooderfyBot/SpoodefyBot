from typing import Optional

from aiohttp import ClientSession


SPOODERFY_WEBSITE_DOMAIN = "spooderfy.com"
SPOODERFY_GATEWAY_DOMAIN = "gateway.spooderfy.com"


class Client:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._session: Optional[ClientSession] = None

    async def setup(self):
        self._session = ClientSession()

    async def teardown(self):
        if self._session is not None:
            await self._session.close()

