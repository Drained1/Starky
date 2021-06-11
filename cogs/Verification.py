import discord
from discord.ext import commands
import os
from urllib.request import urlopen
import json
import requests
import time
import random
import asyncio

def get_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

class Verification(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx, type=None, id=None):
        if type.lower() not in ["kaid", "user"]:
            return await ctx.send("This command should be used like\n```k!verify kaid kaid_................``` or\n```k!verify username kacc```\nThe kaid or username should be yours")

        if not id:
            return await ctx.send("This command should be used like\n```k!verify kaid kaid_................``` or\n```k!verify username kacc```\nThe kaid or username should be yours")

        msg = await ctx.send('Checking if the account exists...')

        if type.lower() == "kaid":
            data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?kaid={id}&format=pretty")
            print(data)

            if data == None:
                return await msg.edit(content="Invalid kaid... Did you include `kaid_` at the beginning? Please try again")
        
        if type.lower() == "user":
            data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?username={id}&format=pretty")
            print(data)

            if data == None:
                return await msg.edit(content="Invalid username... Please try again")

        await msg.edit(content="Account successfully verified!")

        

def setup(client):
    client.add_cog(Verification(client))