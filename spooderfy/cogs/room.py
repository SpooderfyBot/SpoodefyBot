import discord
from typing import Dict, Optional
from discord.ext import commands

from .. import Spooderfy
from .. import spooderfy_api


class GeneralCommands(commands.Cog):
    def __init__(self, bot: Spooderfy):
        self.bot = bot
        self.creator = spooderfy_api.RoomCreator(self.bot.loop)
        self._rooms: Dict[int, spooderfy_api.Room] = {}

    @commands.command(name="createroom")
    @commands.guild_only()
    async def create_room(self, ctx: commands.Context, *, name: str):
        if self._rooms.get(ctx.guild.id):
            return await ctx.reply(
                "Sorry but you already have a room open. "
                "This is a temporary limit and will be removed later."
            )

        new = await ctx.channel.clone(name=f"Movie: {name}")
        buffer = await self.bot.user.avatar.read()
        wh = await new.create_webhook(
            name="Spooderfy Interaction",
            avatar=buffer
        )
        room = await self.creator.create_room(webhook=wh.url, channel=new)
        self._rooms[ctx.guild.id] = room
        return await ctx.reply(f"🎉 Made room: `{room.id}`")

    @create_room.error
    async def create_room_error(self, ctx, exception: Exception):
        exception = getattr(exception, 'original', exception)
        if isinstance(exception, commands.MissingRequiredArgument):
            return await ctx.reply(
                f"**Oops! {exception}**"
            )
        elif isinstance(exception, commands.NoPrivateMessage):
            return await ctx.reply(
                f"**Oops! Sorry but I dont support movies in DMs**")

        elif isinstance(exception, discord.Forbidden):
            return await ctx.reply(
                f"**Oops! Sorry but I dont have permission todo this.\n"
                f"Make sure I have permission to `MANAGE CHANNELS` "
                f"and `MANAGE WEBHOOKS`**")
        raise exception

    @commands.command(name="end", aliases=["deleteroom"])
    @commands.guild_only()
    async def delete_room(self, ctx: commands.Context):
        room = self._rooms.get(ctx.guild.id)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.delete()
        return await ctx.reply(f"🎉 **Deleted room `{room.id}`**")

    @delete_room.error
    async def delete_room_error(self, ctx, exception: Exception):
        if isinstance(exception, commands.NoPrivateMessage):
            return await ctx.reply(
                f"**Oops! Sorry but I dont support movies in DMs**")
        raise exception


def setup(bot: Spooderfy):
    bot.add_cog(GeneralCommands(bot))