import discord
from typing import Optional
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
        room = self.bot.rooms.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        track = spooderfy_api.Track(url=url, title=title or "No Title")
        await room.player.add_track(track)

        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(
            name=f"Added video: {track.title}!",
            icon_url=self.bot.white_icon,
            url=track.url
        )
        await ctx.reply(embed=embed)

    @add_track.error
    async def add_error(self, ctx, exception):
        exception = getattr(exception, 'original', exception)
        if isinstance(exception, commands.MissingRequiredArgument):
            return await ctx.reply(
                "**Oops! You haven't given me a url of the video you "
                "want to add.**"
            )
        raise exception

    @commands.command(name="next", aliases=["n"])
    @commands.guild_only()
    async def next(self, ctx: commands.Context):
        room = self.bot.rooms.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.player.next_track()

    @commands.command(name="previous", aliases=["back"])
    @commands.guild_only()
    async def previous(self, ctx: commands.Context):
        room = self.bot.rooms.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.player.previous_track()

    @commands.command(name="remove", aliases=["rem"])
    @commands.guild_only()
    async def remove(self, ctx: commands.Context, index: int):
        room = self.bot.rooms.get(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.player.remove_track(index)

    @remove.error
    async def remove_error(self, ctx, exception):
        exception = getattr(exception, 'original', exception)
        if isinstance(exception, commands.BadArgument):
            return await ctx.reply(
                "**Oops! You gave me a invalid index, make "
                "sure it is a whole number!**"
            )

        elif isinstance(exception, commands.MissingRequiredArgument):
            return await ctx.reply(
                "**Oops! You haven't given me a index of the video you "
                "want to remove.**"
            )
        raise exception

    @commands.command(name="pause")
    @commands.guild_only()
    async def pause(self, ctx: commands.Context):
        room = self.bot.rooms.get(ctx.guild.id, None)
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
        room = self.bot.rooms.get(ctx.guild.id, None)
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
            ctx.handled = True
            return await ctx.reply(
                f"**Oops! Sorry but I dont support movies in DMs**")
        elif isinstance(exception, discord.Forbidden):
            ctx.handled = True
            return await ctx.author.send(
                f"**Oops! Sorry but I dont have permission todo this.\n"
                f"Make sure I have permission to send messages.")
        elif isinstance(exception, spooderfy_api.HttpException):
            ctx.handled = True
            return await ctx.author.send(
                f"**Oops! I've ran into an error while running this command, "
                f"please try again later.")
        raise exception


def setup(bot: Spooderfy):
    bot.add_cog(PlayerCommands(bot))