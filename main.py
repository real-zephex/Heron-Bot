import asyncio
import os
from pathlib import Path

import discord
from aiohttp import ClientSession
from dotenv import load_dotenv

from bot import Heron
from cogs.utils import HeronLogger, read_env

# Only used for Windows development
if os.name == "nt":
    import winloop

    asyncio.set_event_loop_policy(winloop.WinLoopPolicy())
else:
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

load_dotenv()

TOKEN = os.environ["TOKEN"]
ENV_PATH = Path(__file__).parent / ".env"

intents = discord.Intents.default()
intents.message_content = True


async def main() -> None:
    async with ClientSession() as session:
        async with Heron(
            config=read_env(ENV_PATH), intents=intents, session=session
        ) as bot:
            await bot.start(TOKEN)


def launch() -> None:
    with HeronLogger():
        asyncio.run(main())


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
