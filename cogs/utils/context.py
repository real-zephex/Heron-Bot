from typing import TYPE_CHECKING, Any, Dict, Optional

from aiohttp import ClientSession
from discord.ext import commands

if TYPE_CHECKING:
    from bot import Heron


class HeronContext(commands.Context):
    bot: Heron

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def config(self) -> Dict[str, Optional[str]]:
        """Returns the config for the bot

        This config is directly read from the .env file available

        Returns:
            Dict[str, Optional[str]]: The config for the bot. 1:1 mapping of it
        """
        return self.bot.config

    @property
    def session(self) -> ClientSession:
        """A global web session used throughout the lifetime of the bot

        Returns:
            ClientSession: AIOHTTP ClientSession object
        """
        return self.bot.session

    async def show_help(self, command: Any = None) -> None:
        """Shows the help command for the specified command if given.

        If no command is given, then it'll show help for the current
        command.
        """
        cmd = self.bot.get_command("help")
        command = command or self.command.qualified_name  # type: ignore
        await self.invoke(cmd, command=command)  # type: ignore
