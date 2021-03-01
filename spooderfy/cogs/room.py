from os import getenv
from typing import Dict
from traceback import print_exc

import discord
from discord.ext import commands

from .. import Spooderfy
from .. import spooderfy_api
from .. import pages


class RoomCommands(commands.Cog):
    def __init__(self, bot: Spooderfy):
        self.bot = bot
        self._client = spooderfy_api.Client(str(getenv("API_KEY")))
        self.bot.loop.create_task(self._client.setup())
        self._wait_for_reactions: Dict[int, discord.User] = {}

    @commands.command("create", aliases=["createroom", "cr"])
    async def create_room(self, ctx: commands.Context, *, stream_name: str):
        new: discord.TextChannel = await ctx.channel.clone(name=f"room-{stream_name}")
        buffer = await self.bot.user.avatar_url_as().read()
        wh: discord.Webhook = await new.create_webhook(
            name="Spooderfy Interaction",
            avatar=buffer
        )

        try:
            resp = await self._client.create_room(
                stream_name,
                ctx.author.name,
                ctx.author.id,
                wh.url
            )
        except spooderfy_api.HTTPException as e:
            await ctx.send(discord.utils.escape_mentions(
                f"A unknown error has occurred while handling your request: "
                f"{e!r}"
            ))
            print_exc()

            try:
                await new.delete()
            except:
                pass

            return

        self.bot.rooms[new] = (resp['room_id'], ctx.author.id)

        embed = discord.Embed(
            description=(
                f"• You can join your room by **[clicking me]({resp['url']})**.\n"
                f"• Your room will start streaming when the room owner goes live!\n"
                f"• To close the room simply do `{ctx.prefix}close #{new}`\n"
            ),
            color=self.bot.colour
        )
        embed.set_author(
            name="Welcome to your movie room!",
            icon_url=ctx.author.avatar_url,
        )
        embed.set_footer(
            text=f"Room owned by: {ctx.author}",
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        await wh.send(embed=embed)

        await ctx.send(
            f"🎉 Created room {discord.utils.escape_mentions(stream_name)}!"
        )

        embed = discord.Embed(
            title="Welcome to Spooderfy",
            description=(
                "Now your room is made you'll need these two important links:\n\n"
                f"**Stream Url:**\n"
                f"`{resp['rtmp']}`\n"
                f"(You use this to stream to the room)\n\n"                
                f"**Stream key:**\n "
                f"||`{resp['stream_key']}`|| \n"
                f"(You use this to authorize the stream, **DO NOT SHARE THIS**)\n\n"
                "Simply enter these two details into any streaming system that supports rtmp, "
                "e.g. Streamlabs, OBS, FFMPEG, etc...\n\n"
                "**Need more help? Just react with the** ❓ **emoji for a walk through**"
            ),
            color=self.bot.colour,
        )
        embed.set_image(url="https://i.imgur.com/NjWcxL6.gif")
        msg: discord.Message = await ctx.author.send(
            embed=embed
        )

        await msg.add_reaction("❓")

        self._wait_for_reactions[msg.id] = ctx.author

    @commands.guild_only()
    @commands.command("close", aliases=["closeroom"])
    async def close_room(
            self,
            ctx: commands.Context,
            channel: discord.TextChannel = None,
    ):
        if channel is None:
            channel = ctx.channel

        id_ = self.bot.rooms.get(channel)
        if id_ is None:
            return await ctx.send(
                f"<:tickno:815940376363270185> Channel {channel.name!r} is "
                f"not a streaming room."
            )

        permissions = channel.permissions_for(ctx.author)
        if not permissions.manage_channels and not id_[1]:
            return await ctx.send(
                f"<:tickno:815940376363270185> You are missing permissions to "
                f"run this action, you need either the permission "
                f"`MANAGE_CHANNELS` or be the room owner."
            )

        try:
            await self._client.delete_room(id_[0])
        except spooderfy_api.RoomNotFound:
            pass
        except spooderfy_api.HTTPException:
            print_exc()
            return await ctx.send(
                f"<:tickno:815940376363270185> Oops! I encountered a unknown "
                f"exception while terminating your room please contact "
                f"our support server: *<{self.bot.site_url}/discord>*"
            )

        await channel.delete(reason="room session ended")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        msg = self._wait_for_reactions.get(payload.message_id)

        if msg is None or payload.user_id == self.bot.user.id:
            return

        page = pages.StreamTutorial(self.bot, msg)
        page.start()


def setup(bot: Spooderfy):
    bot.add_cog(RoomCommands(bot))
