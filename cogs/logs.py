import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

wc = os.getenv("welcome_channel")
ml = os.getenv("message_log")


class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # await self.client.get_channel(956266369320624128).send(f"{member.mention} has joined the server")
        embed = discord.Embed(
            title="New Member Joined!! :tada: ",
            description=f"{member.mention} just landed on the server. Welcome them on the server :comet:",
        )
        await self.client.get_channel(wc).send(embed=embed)

    # For commands
    @commands.command()
    @commands.cooldown(rate=2, per=30)
    async def ping(self, ctx):
        await ctx.reply(f"{ctx.message.author.mention} Pong!! :ping_pong:")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in [self.client.user.id, 961676784196255846]:
            return
        embed = discord.Embed(
            title=f"New Message from {message.author.mention}",
            description=f"**Message** : {message.content} ",
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        await self.client.get_channel(int(ml)).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id in [self.client.user.id, 961676784196255846]:
            return
        embed = discord.Embed(
            title=f"Message Deleted from {message.channel}",
            description=f"**Message Deleted** : {message.content}",
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        await self.client.get_channel(int(ml)).send(embed=embed)


def setup(client):
    client.add_cog(Logs(client))
