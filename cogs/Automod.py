import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import random
from random import randint
import asyncio
import motor
import motor.motor_asyncio
from pymongo import MongoClient
import os

user = os.environ.get("user")
passw = os.environ.get("pass")

cluster = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{user}:{passw}@kacc.uozpt.mongodb.net/KACC?retryWrites=true&w=majority")
database = cluster["Discord"]["Automod"]

import dhooks
from dhooks import Webhook

def censor(text, bad_words):
    final = []
    text_split = text.split(" ")
    for word in text_split:
        final_word = word
        if word.lower() in bad_words:
            final.append("\*"*len(word))
        else:
            final.append(word)

    return " ".join(final)

class Automod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        info = await database.find_one({"guild_id":message.guild.id})
        if not info:
            await database.insert_one({"guild_id":message.guild.id, "bad_words":[None]})
            return

        if message.author.bot:
            return
        
        #if message.author.guild_permissions.manage_messages:
            #return

        first_text = message.content.lower().split(" ")
        final = []

        for word in first_text:
            if "\u200b" in word:
                final.append("".join([char for char in word if char != "\u200b"]))
            else:
                final.append(word)
            print(word)
            print(final)

        bad_words = info["bad_words"]

        for a in bad_words:
            if a in final:
                await message.delete()
                a = await message.channel.create_webhook(name = message.author.name)
                await a.send(content = censor(message.content, bad_words), avatar_url = message.author.avatar_url_as(format='png', size=1024))
                await a.delete()
                return

    @commands.command()
    async def blacklist(self, ctx, word):
        if not ctx.author.guild_permissions.manage_messages:
            return
        word = word.lower()

        info = await database.find_one({"guild_id":ctx.guild.id})
        if not info:
            await database.insert_one({"guild_id":ctx.guild.id, "bad_words":[None]})
            return await ctx.send('I had to add your guild to my database. Please retry this command :)')

        if word in info["bad_words"]:
            return await ctx.send('That word is already blacklisted!')

        await database.update_one({"guild_id":ctx.guild.id}, {"$push":{"bad_words":word}})
        await ctx.send(f'Successfully blacklisted {word}')

    @commands.command()
    async def whitelist(self, ctx, word):
        if not ctx.author.guild_permissions.manage_messages:
            return
        word = word.lower()

        info = await database.find_one({"guild_id":ctx.guild.id})
        if not info:
            await database.insert_one({"guild_id":ctx.guild.id, "bad_words":[None]})
            return await ctx.send('I had to add your guild to my database. Please retry this command :)')

        if word not in info["bad_words"]:
            return await ctx.send('That word isnt already blacklisted!')

        await database.update_one({"guild_id":ctx.guild.id}, {"$pull":{"bad_words":word}})
        await ctx.send(f'Successfully whitelisted {word}')

    @commands.command()
    async def blacklists(self, ctx):
        if not ctx.author.guild_permissions.manage_messages:
            return

        info = await database.find_one({"guild_id":ctx.guild.id})
        if not info:
            await database.insert_one({"guild_id":ctx.guild.id, "bad_words":[None]})
            return await ctx.send('I had to add your guild to my database. Please retry this command :)')

        await ctx.send(embed=discord.Embed(title=f"Blacklists in {ctx.guild.name}", description="\n".join(info["bad_words"])))
        

def setup(client):
    client.add_cog(Automod(client))
