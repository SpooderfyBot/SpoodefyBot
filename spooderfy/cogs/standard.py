import discord
import asyncio

from time import perf_counter
from discord.ext import commands

from .. import Spooderfy, utils


HELP_DICT = utils.get_help("help")


class GeneralCommands(commands.Cog):
    def __init__(self, bot: Spooderfy):
        self.bot = bot

    @commands.command(aliases=["h"])
    async def help(self, ctx: commands.Context):

        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(
            icon_url=self.bot.user.avatar_url,
            url=self.bot.site_url,
            name="Spooderfy Basic Help"
        )

        for title, desc in HELP_DICT.items():
            embed.add_field(
                name=title,
                value=desc.format(prefix=self.bot.prefix),
                inline=False
            )

        embed.set_footer(
            text=f"Invoked by {ctx.author}",
            icon_url=ctx.author.avatar_url
        )

        await ctx.reply(embed=embed)


    @commands.command()
    async def ping(self, ctx: commands.Context):
        avg = self.bot.latency * 1000
        shard = self.bot.get_shard(ctx.guild.shard_id).latency * 1000

        start = perf_counter()
        msg = await ctx.reply(
            f"<a:loading:797848379862286376> Checking round trip ping...")
        stop = perf_counter()
        round_trip = (stop - start) * 1000

        await msg.edit(
            content=f"\📡 **Global WS Latency:** `{avg:.0f}ms`\n"
                    f"\📍  **Shard WS Latency:** `{shard:.0f}ms`\n"
                    f"\📬 **Message Latency:** `{round_trip:.0f}ms`\n"
        )


def setup(bot: Spooderfy):
    bot.add_cog(GeneralCommands(bot))