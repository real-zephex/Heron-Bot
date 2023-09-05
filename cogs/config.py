import discord
from discord.ext import commands

from bot import Heron
from cogs.utils import HeronContext


class Config(commands.Cog):
    """Configuration for Heron"""

    def __init__(self, bot: Heron) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    @commands.command(name="toggle")
    @commands.is_owner()
    async def toggle(self, ctx: HeronContext, *, command: str):
        """Enable or disable a command!"""
        command = self.bot.get_command(command)

        if command is None:
            embed = discord.Embed(
                title="ERROR",
                description="I can't find a command with that name!",
                color=0xFF0000,
            )
        elif ctx.command == command:
            embed = discord.Embed(
                title="ERROR",
                description="You cannot disable this command.",
                color=0xFF0000,
            )
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = discord.Embed(
                title="Toggle",
                description=f"I have {ternary} {command.qualified_name} for you!",
                color=0xFF00C8,
            )
        await ctx.send(embed=embed)


async def setup(bot: Heron):
    await bot.add_cog(Config(bot))
