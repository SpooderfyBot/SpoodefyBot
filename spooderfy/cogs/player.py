import discord
from typing import Dict, Optional
from discord.ext import commands

from .. import Spooderfy
from .. import spooderfy_api


class PlayerCommands(commands.Cog):
    def __init__(self, bot: Spooderfy):
        self.bot = bot
        self.creator = spooderfy_api.RoomCreator(self.bot.loop)

    @commands.command(name="addtrack", aliases=["at"])
    @commands.guild_only()
    async def add_track(
        self,
        ctx: commands.Context,
        url: str,
        title: Optional[str] = None,
    ):
        room = self.bot.room.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        track = spooderfy_api.Track(url=url, title=title or "No Title")
        await room.player.add_track(track)
        await ctx.reply(
            f"**Added track [{track.title}]({track.url}) to the queue "
            f"do `{ctx.prefix}next` to cycle the queue.**"
        )

    @commands.command(name="next", aliases=["n"])
    @commands.guild_only()
    async def next(self, ctx: commands.Context):
        room = self.bot.room.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.player.next_track()
        await ctx.reply("**Skipping to next video.**")

    @commands.command(name="pause")
    @commands.guild_only()
    async def pause(self, ctx: commands.Context):
        room = self.bot.room.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.player.pause()
        await ctx.reply("**Paused video**")

    @commands.command(name="play")
    @commands.guild_only()
    async def play(self, ctx: commands.Context):
        room = self.bot.room.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.player.play()
        await ctx.reply("**Starting video**")

    @staticmethod
    async def on_cog_error(ctx, exception):
        exception = getattr(exception, 'original', exception)
        if isinstance(exception, commands.NoPrivateMessage):
            return await ctx.reply(
                f"**Oops! Sorry but I dont support movies in DMs**")
        elif isinstance(exception, discord.Forbidden):
            ctx.handled = True
            return await ctx.author.send(
                f"**Oops! Sorry but I dont have permission todo this.\n"
                f"Make sure I have permission to send messages.")
        raise exception


def setup(bot: Spooderfy):
    bot.add_cog(PlayerCommands(bot))