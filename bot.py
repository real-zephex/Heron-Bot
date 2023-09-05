import logging
import traceback
from typing import Dict, Optional, Union

import discord
from aiohttp import ClientSession
from discord.ext import commands

from cogs import EXTENSIONS
from cogs.utils import ErrorEmbed, HeronContext, HeronHelp


class Heron(commands.Bot):
    """Subclassed bot for HeronBot"""

    def __init__(
        self,
        config: Dict[str, Optional[str]],
        intents: discord.Intents,
        session: ClientSession,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            activity=discord.Game(name="Watching Pheonix's Server"),
            command_prefix=".",
            intents=intents,
            help_command=HeronHelp(),
            *args,
            **kwargs,
        )
        self._config = config
        self._session = session
        self._logger = logging.getLogger("heron")

    @property
    def config(self) -> Dict[str, Optional[str]]:
        """Returns the config for the bot

        This config is directly read from the .env file available

        Returns:
            Dict[str, Optional[str]]: The config for the bot. 1:1 mapping of it
        """
        return self._config

    @property
    def session(self) -> ClientSession:
        """A global web session used throughout the lifetime of the bot

        Returns:
            ClientSession: AIOHTTP ClientSession object
        """
        return self._session

    def build_embed(self, title: str, description: str) -> ErrorEmbed:
        embed = ErrorEmbed()
        embed.title = title
        embed.description = description
        embed.set_footer(text="Happened At")
        return embed

    def build_error_embed(self, error: commands.CommandError) -> ErrorEmbed:
        embed = ErrorEmbed()
        embed.title = "Something went wrong..."
        error_traceback = "\n".join(traceback.format_exception_only(type(error), error))
        desc = (
            "Uh oh! It seems like the command ran into an issue!\n\n"
            f"**Error**: \n```{error_traceback}```"
        )
        embed.description = desc
        return embed

    async def get_context(
        self,
        origin: Union[discord.Interaction, discord.Message],
        /,
        *,
        cls=HeronContext,
    ) -> HeronContext:
        return await super().get_context(origin, cls=cls)

    async def on_command_error(
        self, ctx: HeronContext, error: commands.CommandError
    ) -> None:
        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)

        # silently ignored exceptions
        if isinstance(error, commands.CommandNotFound):
            self._logger.error("Command Not Found (%s)", ctx.message.content)
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=self.build_embed(
                    "Missing Argument(s)",
                    f"You are missing these argument(s): {error.param.name}",
                )
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=self.build_embed(
                    "Command on Cooldown",
                    f"The command is currently on cooldown. Try after {error.retry_after:.2f}",
                )
            )

        elif isinstance(error, commands.MissingPermissions):
            missing_permissions_str = ", ".join(error.missing_permissions).rsplit(",")
            await ctx.send(
                embed=self.build_embed(
                    "Insufficient Permissions",
                    f"You are missing these permissions in order to run the command: {missing_permissions_str}",
                )
            )

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(
                embed=self.build_embed(
                    "Disabled Command", "This command is disabled for now"
                )
            )

        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                embed=self.build_embed(
                    "You can't access these commands", "These commands are owner only"
                )
            )
        else:
            await ctx.send(embed=self.build_error_embed(error))

    async def setup_hook(self) -> None:
        """Setup hook to do anything before the bot starts up"""
        for extension in EXTENSIONS:
            await self.load_extension(extension)

    async def on_ready(self) -> None:
        """When the bot is fully ready, we will do some logging here

        DO NOT ADD STUFF HERE!
        """
        self._logger.info("Heron is ready")
