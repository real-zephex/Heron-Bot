import random

import discord
from discord.ext import commands

from bot import Heron
from cogs.utils import HeronContext

RPS_LIST = ["rock", "paper", "scissor"]


class Fun(commands.Cog):
    """Some fun commands to mess around with"""

    def __init__(self, bot: Heron) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f604")

    @commands.command()
    async def slap(self, ctx: HeronContext, member: discord.Member):
        await ctx.reply(
            f"{member.mention} was slapped by {ctx.message.author.mention}",
            file=discord.File("images/pngtree-slap-emoji-png-image_2828294.jpg"),
        )

    @commands.command()
    async def rps(self, ctx: HeronContext, *, choice):
        if ctx.channel.id != int(ctx.config["RPS_ID"]):  # type: ignore
            return

        if choice not in RPS_LIST:
            await ctx.message.delete()
            return

        random_choice = random.choice(RPS_LIST)

        if choice == random_choice:
            c = "Game Tied"

        elif (
            choice == "rock"
            and random_choice == "scissor"
            or choice == "scissor"
            and random_choice == "paper"
            or choice == "paper"
            and random_choice == "rock"
        ):
            c = f"{ctx.author.mention} Won!!"

        else:
            c = "Heron Won"

        embed = discord.Embed(
            title="Rock Paper Scissor!!",
            description=f"**{ctx.author}** : {choice}\n**Heron** : {random_choice} ",
        )
        embed.add_field(name="Result", value=c)
        await ctx.reply(embed=embed)

    @commands.command()
    async def meme(self, ctx: HeronContext):
        if ctx.channel.id != int(ctx.config["MEME_CHANNEL_ID"]):
            return

        params = {"sort": "hot"}
        async with ctx.session.get(
            "https://www.reddit.com/r/dankmemes/new.json", params=params
        ) as r:
            res = await r.json()
            image_url = res["data"]["children"][random.randint(0, 25)]["data"]["url"]
            embed = discord.Embed()
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Ordered by : {ctx.author} | {ctx.author.id}")
            await ctx.send(embed=embed)


async def setup(bot: Heron):
    await bot.add_cog(Fun(bot))
