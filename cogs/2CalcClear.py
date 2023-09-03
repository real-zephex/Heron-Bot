import discord
from discord.ext import commands


class cog_2(commands.Cog):
    def __init__(self, client):
        self.client = client

    # clear channel
    @commands.command()
    async def clear(self, ctx, amount=5):
        if amount > 1000:
            await ctx.reply("Please delete messages in limited amount. Deleting large amount of messages may lag the server")
            return
        if ctx.message.author.guild_permissions.manage_channels:
            await ctx.channel.purge(limit=amount)
            embed2 = discord.Embed(
                title="Channel Purged",
                color=0x465722,
                description=f"{ctx.channel.mention} has been purged by {ctx.message.author.mention} ",
            )
            await ctx.send(embed=embed2)
        else:
            embed3 = discord.Embed(
                title="Permissions Error",
                description=f"{ctx.message.author.mention} You don't have sufficient permissions to execute that command ",
            )
            await ctx.reply(embed=embed3)


def setup(client):
    client.add_cog(cog_2(client))
