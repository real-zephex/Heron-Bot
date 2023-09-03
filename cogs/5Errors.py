import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()


class cog_5(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)

        # silently ignored exceptions
        if isinstance(error, (commands.CommandNotFound)):
            print(f"[Handled] Command Not Found Error {ctx.message.content} ")
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Arguements Missing",
                description="Important arguements are missing",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Command on Cooldown",
                description=f"The command **{ctx.message.content}** is currently on cooldoown. Try after some time",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Insufficient Permissions",
                value="You are missing permissions to execute that command",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                title="Disabled Command",
                description="This command is disable for now. ",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="You can't access these commands",
                description="These commands are owner only",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                title="Invoke Error",
                description="Some error occured during the execution. Check the format of the command",
            )
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MessageNotFound):
            print("Unknown message found")
        else:
            print(error)


def setup(client):
    client.add_cog(cog_5(client))
