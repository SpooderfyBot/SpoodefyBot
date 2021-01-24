import discord
from discord.ext import commands

from .. import Spooderfy
from .. import spooderfy_api


class RoomCommands(commands.Cog):
    def __init__(self, bot: Spooderfy):
        self.bot = bot
        self.creator = spooderfy_api.RoomCreator(self.bot.loop)

    @commands.command(name="createroom")
    @commands.guild_only()
    async def create_room(self, ctx: commands.Context, *, name: str):
        if self.bot.room.get(ctx.guild.id):
            return await ctx.reply(
                "Sorry but you already have a room open. "
                "This is a temporary limit and will be removed later."
            )

        new = await ctx.channel.clone(name=f"movie-{name}")
        buffer = await self.bot.user.avatar_url_as().read()
        wh: discord.Webhook = await new.create_webhook(
            name="Spooderfy Interaction",
            avatar=buffer
        )
        room = await self.creator.create_room(webhook=wh.url, channel=new)
        self.bot.room[ctx.guild.id] = room

        welcome = discord.Embed(
            title="Welcome to the movie room!",
            description=f"Some info and commands you might want:",
            colour=self.bot.colour,
        )
        welcome.add_field(
            name="Room Link",
            value=f"[Click me to join]({self.bot.site_url}/room/{room.id})",
            inline=False,
        )
        welcome.add_field(
            name="Useful Commands",
            value=f"- `{ctx.prefix}addtrack <video url> <video name (optional)>`\n"
                  f"- `{ctx.prefix}removetrack <video index>`\n"
                  f"- `{ctx.prefix}next`\n"
                  f"- `{ctx.prefix}previous`\n"
                  f"- `{ctx.prefix}play`\n"
                  f"- `{ctx.prefix}pause`\n"
        )
        welcome.set_thumbnail(url=self.bot.user.avatar_url)
        welcome.set_footer(
            text=f"{ctx.author} is the owner of this room.",
            icon_url=ctx.author.avatar_url,
        )
        await wh.send(embed=welcome)

        return await ctx.reply(f"🎉 Made room: `{room.id}`")

    @create_room.error
    async def create_room_error(self, ctx, exception):
        exception = getattr(exception, 'original', exception)
        if isinstance(exception, commands.MissingRequiredArgument):
            return await ctx.reply(f"**Oops! {exception}**")
        elif isinstance(exception, commands.NoPrivateMessage):
            return await ctx.reply(
                f"**Oops! Sorry but I dont support movies in DMs**")

        elif isinstance(exception, discord.Forbidden):
            ctx.handled = True
            return await ctx.reply(
                f"**Oops! Sorry but I dont have permission todo this.\n"
                f"Make sure I have permission to `MANAGE CHANNELS` "
                f"and `MANAGE WEBHOOKS`**")
        raise exception

    @commands.command(name="end", aliases=["deleteroom"])
    @commands.guild_only()
    async def delete_room(self, ctx: commands.Context):
        room = self.bot.room.pop(ctx.guild.id, None)
        if not room:
            return await ctx.reply(
                "**Sorry but you don't have a room created.\n"
                f"To make a room run: `{ctx.prefix}createroom <room name>`**"
            )

        await room.delete()
        return await ctx.reply(f"🎉 **Deleted room `{room.id}`**")

    @delete_room.error
    async def delete_room_error(self, ctx, exception: Exception):
        exception = getattr(exception, 'original', exception)
        if isinstance(exception, commands.NoPrivateMessage):
            return await ctx.reply(
                f"**Oops! Sorry but I dont support movies in DMs**")
        elif isinstance(exception, discord.Forbidden):
            ctx.handled = True
            return await ctx.reply(
                f"**Oops! Sorry but I dont have permission todo this.\n"
                f"Make sure I have permission to `MANAGE CHANNELS` "
                f"and `MANAGE WEBHOOKS`**")
        raise exception


def setup(bot: Spooderfy):
    bot.add_cog(RoomCommands(bot))