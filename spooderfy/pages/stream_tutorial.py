import asyncio
import discord
from discord.ext import commands

from spooderfy.bot import Spooderfy


RTMP_ARTICLE = "https://www.dacast.com/blog/video-streaming-software/"

STREAM_LABS = "https://streamlabs.com/obs/download"
OBS = "https://obsproject.com/download"
FFMPEG = "https://ffmpeg.org/download.html"


STREAM_LABS_GIF = "https://i.imgur.com/NjWcxL6.gif"
OBS_GIF = "https://i.imgur.com/4Yn7UZD.gif"
FFMPEG_GIF = "https://i.imgur.com/MKrPNz5.gif"


class Emojis:
    ONE = "1️⃣"
    TWO = "2️⃣"
    THREE = "3️⃣"
    CUSTOM = "🛠️"

    EMOJIS = (ONE, TWO, THREE, CUSTOM)

    @classmethod
    def contains(cls, item) -> bool:
        return item in cls.EMOJIS


STAGE_1 = discord.Embed(
    title="Streaming Tutorial",
    description=(
        "Hello! Welcome to the tutorial for getting your movie "
        "room up and running!\n"
        "Its straight forward simply choose a RTMP capable streaming software, "
        f"if you do not know what this is take a look at [this article]({RTMP_ARTICLE})\n"
        "(Any software that you can stream to Twitch.tv with.)\n\n"
        "The Spooderfy team recommend either:\n"
        f"**1) [Streamlabs OSB]({STREAM_LABS}) (easy)**\n"
        f"**2) [OBS]({OBS}) (medium)**\n"
        f"**3) [FFmpeg]({FFMPEG}) (hard)**\n"
        "depending on your pre-existing knowledge.\n"
        "If you've downloaded one of these three,\n ⚠️**click "
        "on one of the numbered emojis from 1 - 3 otherwise click on the 🛠️ emoji.**"
    ),
    color=Spooderfy.colour
)

STAGE_2_STREAM_LABS = discord.Embed(
    title="Streaming Tutorial - Streamlabs",
    description=(
        "You chose Streamlabs, excellent choice!\n\n"
        "**Instructions**\n"
        "- Go to the settings page located in the bottom "
        "left corner of your window.\n"
        "- Go to the section in settings called *'Stream'*\n"
        "- Select the `Custom Streaming Server` option on the *'Stream Type'* field\n"
        "- Enter the RTMP url you have been given in the *'URL'* field\n"
        "- Enter the given stream key in the *'Stream key'* field\n"
        "- Click *'Done'*\n"
        "\n"
        "**Congratulations! You're all setup and ready to go!**\n"
    ),
    color=Spooderfy.colour
)
STAGE_2_STREAM_LABS.set_image(url=STREAM_LABS_GIF)

STAGE_2_OSB = discord.Embed(
    title="Streaming Tutorial - OBS",
    description=(
        "You chose OBS, excellent choice!\n\n"
        "**Instructions**\n"
        "- Go to the settings page located in the bottom "
        "right corner of your window.\n"
        "- Go to the section in settings called *'Stream'*\n"
        "- Select the `Custom...` option on the *'Service'* field\n"
        "- Enter the RTMP url you have been given in the *'Server'* field\n"
        "- Enter the given stream key in the *'Stream key'* field\n"
        "- Click *'Done'*\n"
        "\n"
        "**Congratulations! You're all setup and ready to go!**\n"
    ),
    color=Spooderfy.colour
)
STAGE_2_OSB.set_image(url=OBS_GIF)

STAGE_2_FFMPEG = discord.Embed(
    title="Streaming Tutorial - FFmpeg",
    description=(
        "You chose FFmpeg, a fine choice to those who can master the beast!\n\n"
        "**Instructions**\n"
        "*FFmpeg is a very large and diverse tool, these instructions only give"
        " a basic approach to streaming to us.*\n"
        "Command: `ffmpeg -re -i <myfile>.flv -c copy -f flv <rtmp url>/<stream key>`\n"
        "`-re` - Used the native video framerate\n"
        "`-i <file>` - The input file\n"
        "`-c <options>` - The video codec settings, `copy` simply copies\n"
        "`-f <format>` - The format to re-encode the video into\n"
        "**Congratulations! You're streaming to our servers when the commands is ran, "
        "note that you can customise these options a near infinite amount.**"
    ),
    color=Spooderfy.colour
)
STAGE_2_FFMPEG.set_image(url=FFMPEG_GIF)

STAGE_2_CUSTOM = discord.Embed(
    title="Streaming Tutorial - Custom",
    description=(
        "You chose a custom streaming server!\n\n"
        "**Basic Instructions**\n"
        "*Due to the nature of each custom server being different we cannot "
        "provide exact instructions on how to stream to us.*\n"
        "- Select custom streaming server / server url\n"
        "- Enter given url\n"
        "- Enter given stream key\n"
        "**Congratulations! You're ready!**"

    ),
    color=Spooderfy.colour
)


class StreamTutorial:
    def __init__(self, bot: Spooderfy, user: discord.User):
        self._bot = bot
        self._user = user

    def start(self):
        asyncio.create_task(self.handle_run())

    async def handle_run(self):
        try:
            await self._run()
        except discord.Forbidden:
            return

    async def _run(self):
        msg = await self._user.send(embed=STAGE_1)

        for emoji in Emojis.EMOJIS:
            await msg.add_reaction(emoji)

        def check(p: discord.RawReactionActionEvent):
            return (
                    (p.message_id == msg.id)
                    and Emojis.contains(str(p.emoji))
                    and (p.user_id == self._user.id)
            )

        try:
            payload: discord.RawReactionActionEvent = await self._bot.wait_for(
                "raw_reaction_add",
                check=check,
                timeout=60,
            )
        except asyncio.TimeoutError:
            await self._user.send(
                "The help menu has timed out, to get the menu "
                "back simply re-click the question mark"
            )
            return

        emoji = str(payload.emoji)

        await msg.clear_reactions()

        if emoji == Emojis.ONE:
            await msg.edit(embed=STAGE_2_STREAM_LABS)
        elif emoji == Emojis.TWO:
            await msg.edit(embed=STAGE_2_OSB)
        elif emoji == Emojis.THREE:
            await msg.edit(embed=STAGE_2_FFMPEG)
        elif emoji == Emojis.CUSTOM:
            await msg.edit(embed=STAGE_2_CUSTOM)
