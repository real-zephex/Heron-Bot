import logging

import discord
from aiohttp import ClientSession
from discord.ext import commands

from cogs import EXTENSIONS
from cogs.utils import HeronHelp


class Heron(commands.Bot):
    """Subclassed bot for HeronBot"""

    def __init__(
        self, intents: discord.Intents, session: ClientSession, *args, **kwargs
    ) -> None:
        super().__init__(
            command_prefix=".",
            intents=intents,
            help_command=HeronHelp(),
            *args,
            **kwargs
        )
        self._session = session
        self._logger = logging.getLogger("heron")

    @property
    def session(self) -> ClientSession:
        """A global web session used throughout the lifetime of the bot

        Returns:
            ClientSession: AIOHTTP ClientSession object
        """
        return self._session

    async def setup_hook(self) -> None:
        """Setup hook to do anything before the bot starts up"""
        for extension in EXTENSIONS:
            await self.load_extension(extension)

    async def on_ready(self) -> None:
        """When the bot is fully ready, we will do some logging here

        DO NOT ADD STUFF HERE!
        """
        self._logger.info("Heron is ready")
