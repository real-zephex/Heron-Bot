from typing import Optional

import discord
from discord.ext import commands

from bot import Heron
from cogs.utils import HeronContext


class Admin(commands.Cog):
    """Administrative management module"""

    def __init__(self, bot: Heron) -> None:
        self.bot = bot

    # WARNING!!!
    # This will load ALL of the words into memory, thus eatting up a ton of your RAM
    # AND plus this code is I/O intensive and blocking, thus blocking any other commands from being ran, making your bot completely useless while that is being ran
    # And what makes it even worse is that this is done on EVERY SINGLE MESSAGE BEING SENT ON EVERY SINGLE SERVER THAT THIS BOT IS IN
    # I urge you to instead use Regex for this, and just DO NOT do this anymore
    # Your code is filled with bad practices
    # - Noelle
    def swear_words(self):
        with open("swear_words.txt", "r") as file:
            data = file.read()
            return data.split("\n")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:blobban:759935431847968788>")

    @commands.command()
    async def clear(self, ctx: HeronContext, amount: int = 5):
        """Clears any messages with a specified amount"""
        if amount > 1000:
            await ctx.reply(
                "Please delete messages in limited amount. Deleting large amount of messages may lag the server"
            )
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

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: HeronContext, member: discord.Member, *, reason=None):
        """Kick a member out of the server"""
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
        await self.bot.get_channel(abl).send(embed=embed9)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx: HeronContext, member: discord.Member, *, reason: Optional[str] = None
    ):
        """Ban a member"""
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
        await self.bot.get_channel(abl).reply(embed=embed10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx: HeronContext, member: discord.Member, *, reason=None):
        """Mute a member"""
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
    async def unmute(self, ctx: HeronContext, member: discord.Member):
        """Unmute a user"""
        muted_role = ctx.guild.get_role(int(mr))
        embed = discord.Embed(
            title="Member unmuted",
            description=f"{ctx.message.author.mention} used unmute command",
        )
        embed.add_field(name=f"**Member Unmuted **: {member}", value="Behave")
        await member.remove_roles(muted_role)
        await ctx.reply(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx: HeronContext, extension: str):
        """Reload the ext"""
        await self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send("Successfully Reloaded! :white_check_mark: ")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if any(word in message.content for word in self.swear_words()):
            await message.delete()
            embed7 = discord.Embed(
                title="New Abuser Found",
                description=f"{message.author.mention} used the swear word **{message.content}**. \nAlthough **the message was deleted** ",
            )
            await self.bot.get_channel(int(al)).send(embed=embed7)

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Insufficient Permissions",
                color=0x465722,
                description="You dont have permissions to reload cogs",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Cog needs to be attached",
                description="Command is : .reload <cog name>",
            )
            await ctx.send(embed=embed)


async def setup(bot: Heron):
    await bot.add_cog(Admin(bot))
