import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

abl = os.getenv("kick_ban_log")
mr = os.getenv("muted_role_id")

class cog_4(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed4 = discord.Embed(
            title="Member Kicked",
            color=0x465722,
            description=f"{member.mention} has been kicked from the server by {ctx.message.author.mention} for reason {reason}.",
        )
        await ctx.reply(embed=embed4)
        embed9 = discord.Embed(
            title="User Kicked",
            description=f"User : {member.mention}\nReason : {reason}",
        )
        await self.client.get_channel(abl).send(embed=embed9)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed3 = discord.Embed(
            title="Member Banned",
            color=0x465722,
            description=f"{member} has been banned from the server by {self.message.author.mention} for reason {reason}.",
        )
        await ctx.reply(embed=embed3)
        embed10 = discord.Embed(
            title="User Banned",
            description=f"User : {member.mention}\nReason : {reason}",
        )
        await self.client.get_channel(abl).reply(embed=embed10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):

        muted_role = ctx.guild.get_role(int(mr))
        embed = discord.Embed(
            title="Member Muted",
            description=f"{ctx.message.author.mention} used mute command",
        )
        embed.add_field(
            name=f"**Member Muted **: {member}",
            value=f"**Reason** : {reason}",
        )
        await member.add_roles(muted_role)
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):

        muted_role = ctx.guild.get_role(int(mr))
        embed = discord.Embed(
            title="Member unmuted",
            description=f"{ctx.message.author.mention} used unmute command",
        )
        embed.add_field(name=f"**Member Unmuted **: {member}", value="Behave")
        await member.remove_roles(muted_role)
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(cog_4(client))

