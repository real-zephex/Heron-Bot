import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

al = os.getenv("abuse_log")

def swear_words():
    with open("Docs/swear_words.txt", "r") as file:
        data = file.read()
        return data.split("\n")


class cog_3(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return

        if any(word in message.content for word in swear_words()):
            await message.delete()
            embed7 = discord.Embed(
                title="New Abuser Found",
                description=f"{message.author.mention} used the swear word **{message.content}**. \nAlthough **the message was deleted** ",
            )
            await self.client.get_channel(int(al)).send(embed=embed7)
        
        

def setup(client):
    client.add_cog(cog_3(client))
