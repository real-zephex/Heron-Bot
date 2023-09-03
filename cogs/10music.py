import discord
from discord.ext import commands
import yt_dlp as yt
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

mc = os.getenv("music_channel_id")
yt.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "Music/%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "10.0.0.2",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = yt.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )
        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]
        return data["title"] if stream else ytdl.prepare_filename(data)


class cog_10(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.channel.id != int(mc):
            return

        if not ctx.message.author.voice:
            await ctx.reply(
                f"{ctx.message.author.mention} is not connected to any voice channel"
            )
            return

        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    @commands.command()
    async def leave(self, ctx):

        if ctx.channel.id != int(mc):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()

        else:
            await ctx.reply("The bot is not connected to any voice channel")


    @commands.command()
    async def play(self, ctx, *, url):
        if ctx.channel.id != int(mc):
            return
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=self.client.loop)
                voice_channel.play(
                    discord.FFmpegPCMAudio(
                        executable="/usr/bin/ffmpeg", source=filename
                    )
                )
                x = str(filename[:-5]).replace("_", " ").upper().replace("MUSIC/", "")
                await ctx.reply(f"**Now playing:** {x}")

        except Exception:

            embed = discord.Embed(
                title="Queue Feature not available",
                description="Queue feature is not available yet. But it will be available soon",
            )

            await ctx.reply(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        if ctx.channel.id != int(mc):
            return
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.reply("The bot is not playing anything at the moment.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.channel.id != int(mc):
            return
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.reply(
                "The bot was not playing anything before this. Use play_song command"
            )

    @commands.command()
    async def stop(self, ctx):
        if ctx.channel.id != int(mc):
            return
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.reply("The bot is not playing anything at the moment.")


def setup(client):
    client.add_cog(cog_10(client))
