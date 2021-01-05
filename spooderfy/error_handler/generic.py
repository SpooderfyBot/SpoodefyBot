import discord

from .. import utils


PERMISSIONS_MESSAGE = utils.load_md("permissions")


async def missing_permissions(ctx):
    try:
        return await ctx.send(PERMISSIONS_MESSAGE)
    except discord.Forbidden:
        pass

    try:
        return await ctx.author.send(PERMISSIONS_MESSAGE)
    except discord.Forbidden:
        # Give up, just ignore them.
        return
