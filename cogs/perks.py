import logging

import discord
import sqlite3
import db

from discord.ext import commands
class Perks(commands.Cog):
    def __init__(self, client): 
        self.client = client

    @commands.command()
    async def on_raw_reaction_add(self, payload):
        mssgId = payload.message_id
        if mssgId == roleMessage.id:
            guildId = payload.guild_id
            guild = discord.utils.find(lambda currentGuild: currentGuild.id == guildId, self.client.guilds)
            


    @commands.command()
    async def perks(self, ctx):
        currentUser = ctx.author
        roleMessage = await ctx.send("React with one of the emotes corresponding to the perk you want, {}:\n")

def setup(client):
    client.add_cog(Perks(client))
