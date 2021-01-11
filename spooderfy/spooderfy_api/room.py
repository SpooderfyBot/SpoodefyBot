import discord

from .abc import BaseInteraction, BaseRequester
from .request import Requester, Methods
from .exceptions import HttpException
from .utils import create_room_id
from .player import Player


BASE_EXTENSION = "/room"


class RoomCreator(BaseRequester):
    def __init__(self, loop):
        requester = Requester(loop)
        super().__init__(requester)

    async def create_room(
            self,
            webhook: str,
            channel: discord.TextChannel,
    ) -> "Room":
        payload = {
            "webhook": webhook
        }

        room_id = create_room_id()
        url = f"{BASE_EXTENSION}/{room_id}/create"

        resp = await self.request(Methods.POST, url, json=payload)

        if resp != 200:
            raise HttpException(
                "Operation 'play' did not respond with 200 code.")

        return Room(
            room_id=room_id,
            channel=channel,
            requester=self._requester
        )


class Room(BaseInteraction):
    def __init__(
            self,
            room_id: str,
            channel: discord.TextChannel,
            requester: Requester,
    ):
        super().__init__(room_id, requester)

        self.player = Player(room_id, requester)
        self.channel = channel

    async def delete(self):
        await self.channel.delete()

        url = f"{BASE_EXTENSION}/{self.room_id}/create"

        resp = await self.request(Methods.DEL, url)

        if resp != 200:
            raise HttpException(
                "Operation 'play' did not respond with 200 code.")

    def __repr__(self):
        return f"Room(id={self.room_id})"

    @property
    def id(self):
        return self.room_id
