import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


class cog_11(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        await ctx.reply(
            f"{member.mention} was slapped by {ctx.message.author.mention}",
            file=discord.File("images/pngtree-slap-emoji-png-image_2828294.jpg")
        )


def setup(client):
    client.add_cog(cog_11(client))
