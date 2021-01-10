import discord

from typing import Optional
from functools import lru_cache


@lru_cache()
def get_mentions(id_: int) -> set:
    return {f"<@{id_}>", f"<@!{id_}>"}


async def acquire_prefix(guild: Optional[discord.Guild]) -> None:
    return None



