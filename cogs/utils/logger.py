import logging
from logging.handlers import RotatingFileHandler
from types import TracebackType
from typing import Optional, Type, TypeVar

import discord

BE = TypeVar("BE", bound=BaseException)

STARTUP_MESSAGE = """
Welcome to Heron Bot! 
This bot is currently under development and it is bound to get delayed!
Made by : Phoenix, and heavily improved by Noelle (No767)
"""


class HeronLogger:
    def __init__(self) -> None:
        self.self = self
        self.log = logging.getLogger("heron")

    def __enter__(self) -> None:
        max_bytes = 32 * 1024 * 1024  # 32 MiB
        self.log.setLevel(logging.INFO)
        logging.getLogger("discord").setLevel(logging.INFO)
        handler = RotatingFileHandler(
            filename="heron.log",
            encoding="utf-8",
            mode="w",
            maxBytes=max_bytes,
            backupCount=5,
        )
        self.log.addHandler(handler)
        discord.utils.setup_logging()
        self.log.info(STARTUP_MESSAGE)

    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        handlers = self.log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            self.log.removeHandler(hdlr)
