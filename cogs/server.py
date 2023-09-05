import discord
from discord.ext import commands

from bot import Heron
from cogs.utils import HeronContext


class Server(commands.Cog):
    """Server related commands"""

    def __init__(self, bot: Heron):
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    @commands.command()
    async def rules(self, ctx: HeronContext):
        embed = discord.Embed(
            title="Rules", description="Never try to break these rules", colour=0x87CEEB
        )
        embed.add_field(
            name="1. No Swearing",
            value="Messages containing swear words are automatically deleted",
            inline=False,
        )
        embed.add_field(
            name="2. No GhostPings", value="Ghostpings are discouraged", inline=False
        )
        embed.add_field(
            name="3. Bugs/Glitches found should be reported immediately",
            value="There are many",
            inline=False,
        )

        embed.set_author(
            name="heron", icon_url="https://avatars.githubusercontent.com/u/16879430"
        )
        embed.set_footer(
            text="We are watching you!!",
            icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png",
        )
        await ctx.send(embed=embed)


async def setup(bot: Heron):
    await bot.add_cog(Server(bot))
