import asyncio

from typing import Optional
from asyncio import get_event_loop
from datetime import timedelta

from aiohttp import ClientSession, ClientResponse

SPOODERFY_WEBSITE_DOMAIN = "spooderfy.com"
SPOODERFY_BASE_URL = "https://spooderfy.com"

CREATE_ROOM = f"{SPOODERFY_BASE_URL}/api/create/room"
DELETE_ROOM = f"{SPOODERFY_BASE_URL}/api/room/{{}}/delete"


MAX_ROOM_TIME = timedelta(hours=2)


class HTTPException(Exception):
    """ A base http exception """


class RoomNotFound(HTTPException):
    """ Room not found """


class Client:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._session: Optional[ClientSession] = None

    async def setup(self):
        self._session = ClientSession()

    async def teardown(self):
        if self._session is not None:
            await self._session.close()

    async def _request(self, method: str, url: str, **extra) -> ClientResponse:
        headers = {"Authorization": self._api_key}
        return await self._session.request(method, url, headers=headers, **extra)

    async def create_room(
            self,
            stream_name: str,
            owner_name: str,
            owner_id: int,
            webhook_url: str,
    ):
        payload = {
            "webhook_url": webhook_url,
            "owner_name": owner_name,
            "owner_id": owner_id,
            "stream_name": stream_name,
        }

        resp = await self._request("POST", CREATE_ROOM, json=payload)
        resp.raise_for_status()

        details = await resp.json()
        data = details['data']

        room_id = data['url'].replace(f"{SPOODERFY_BASE_URL}/room/", "")
        data['room_id'] = room_id

        get_event_loop().call_later(
            MAX_ROOM_TIME.total_seconds(),
            self._room_expire,
            room_id,
        )

        return data

    def _room_expire(self, room_id: str):
        asyncio.create_task(self.delete_room(room_id))

    async def delete_room(self, room_id: str):
        resp = await self._request("DELETE", DELETE_ROOM.format(room_id))
        if resp.status == 404:
            raise RoomNotFound(f'room with id {room_id!r} not found')
        raise HTTPException(
            f'unknown invalid status raised {resp.status!r}, {await resp.read()}')

