import discord
from discord.utils import utcnow


class ErrorEmbed(discord.Embed):
    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(214, 6, 6))
        kwargs.setdefault("timestamp", utcnow())
