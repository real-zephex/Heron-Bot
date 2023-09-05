import discord
from discord.ext import commands

from bot import Heron


class Logs(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="New Member Joined!! :tada: ",
            description=f"{member.mention} just landed on the server. Welcome them on the server :comet:",
        )
        await self.bot.get_channel(self.bot.config["WELCOME_CHANNEL_ID"]).send(
            embed=embed
        )

    # For commands
    @commands.command()
    @commands.cooldown(rate=2, per=30)
    async def ping(self, ctx):
        await ctx.reply(f"{ctx.message.author.mention} Pong!! :ping_pong:")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in [self.bot.user.id, 961676784196255846]:
            return
        embed = discord.Embed(
            title=f"New Message from {message.author.mention}",
            description=f"**Message** : {message.content} ",
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        await self.bot.get_channel(int(self.bot.config["MESSAGE_LOG"])).send(
            embed=embed
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id in [self.bot.user.id, 961676784196255846]:
            return
        embed = discord.Embed(
            title=f"Message Deleted from {message.channel}",
            description=f"**Message Deleted** : {message.content}",
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        await self.bot.get_channel(int(self.bot.config["MESSAGE_LOG_ID"])).send(
            embed=embed
        )


async def setup(bot: Heron):
    await bot.add_cog(Logs(bot))
