import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()


class cog_12(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, user: discord.Member, *, message=None):
        embed = discord.Embed(
            title=f"Message from {ctx.author.name}",
            description=f"{message}"
            )
        await user.send(embed=embed)


def setup(client):
    client.add_cog(cog_12(client))
