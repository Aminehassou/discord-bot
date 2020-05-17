import logging
import discord
import sqlite3
import db
from discord.ext import commands

class Items(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.items = {}
        tempItems = db.getItems()
        for item in tempItems:
            self.items[item["item_id"]] = item
    
    @commands.command()
    async def steal(self, ctx, user):
        userId = ctx.author.id
        guildId = ctx.author.guild.id
        if db.getUserItem(3, userId, guildId) is not None:


def setup(client):
    client.add_cog(Items(client))