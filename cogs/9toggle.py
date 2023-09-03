import discord
from discord.ext import commands

class cog_9(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.client.get_command(command)

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


def setup(client):
    client.add_cog(cog_9(client))
