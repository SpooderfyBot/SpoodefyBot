from dataclasses import dataclass


@dataclass()
class Track:
    title: str
    url: str


@dataclass()
class Message:
    content: str
    user_id: int
    username: str
    avatar: str



