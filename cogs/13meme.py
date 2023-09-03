import discord
from discord.ext import commands
import random
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

meme = os.getenv("meme_channel_id")

class cog_13(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def meme(self, ctx):
		if ctx.channel.id != int(meme):
			return

		embed = discord.Embed(
			title = "",
			description = ""
		)
		async with aiohttp.ClientSession() as session:
			async with session.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
				res = await r.json()
				embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
				embed.set_footer(
					text = f"Ordered by : {ctx.author} | {ctx.author.id}"
				)
				await ctx.send(embed=embed)


def setup(bot:commands.Bot):
	bot.add_cog(cog_13(bot))