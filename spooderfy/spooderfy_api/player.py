from .abc import BaseInteraction
from .request import Requester, Methods
from .exceptions import HttpException
from .models import Track


class Player(BaseInteraction):
    BASE_EXTENSION = "/player"

    def __init__(self, room_id: str, requester: Requester):
        super().__init__(room_id, requester)

    async def play(self):
        url = f"{self.BASE_EXTENSION}/{self.room_id}/play"
        resp = await self.request(Methods.PUT, url)
        if resp.status != 200:
            raise HttpException(
                "Operation 'play' did not respond with 200 code.")

    async def pause(self):
        url = f"{self.BASE_EXTENSION}/{self.room_id}/pause"
        resp = await self.request(Methods.PUT, url)
        if resp.status != 200:
            raise HttpException(
                "Operation 'pause' did not respond with 200 code.")

    async def seek(self, time: int):
        url = f"{self.BASE_EXTENSION}/{self.room_id}/seek?position={time}"
        resp = await self.request(Methods.PUT, url)
        if resp.status != 200:
            raise HttpException(
                "Operation 'seek' did not respond with 200 code.")

    async def add_track(self, track: Track):
        url = f"{self.BASE_EXTENSION}/{self.room_id}/track/add"
        resp = await self.request(Methods.POST, url, json=track.__dict__)
        if resp.status != 200:
            raise HttpException(
                f"Operation 'add_video' did not respond with 200 code:\n"
                f"{resp.status} {await resp.json()}")

    async def remove_track(self, index: int):
        url = f"{self.BASE_EXTENSION}/{self.room_id}/track/remove?index={index}"
        resp = await self.request(Methods.DEL, url)
        if resp.status != 200:
            raise HttpException(
                "Operation 'remove_track' did not respond with 200 code.")

    async def next_track(self):
        url = f"{self.BASE_EXTENSION}/{self.room_id}/track/next"
        resp = await self.request(Methods.PUT, url)
        if resp.status != 200:
            raise HttpException(
                "Operation 'remove_track' did not respond with 200 code.")

    async def previous_track(self):
        url = f"{self.BASE_EXTENSION}/{self.room_id}/track/previous"
        resp = await self.request(Methods.PUT, url)
        if resp.status != 200:
            raise HttpException(
                "Operation 'remove_track' did not respond with 200 code.")
