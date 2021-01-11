
from .request import Requester


class BaseRequester:
    def __init__(self, requester: Requester):
        self._requester = requester

    @property
    def request(self):
        return self._requester.request


class BaseInteraction(BaseRequester):
    def __init__(self, room_id: str, requester: Requester):
        super().__init__(requester)
        self._room_id = room_id

    @property
    def room_id(self):
        return self._room_id


