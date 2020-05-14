import logging
import discord
import sqlite3
import db

from discord.ext import commands
class Shop(commands.Cog):
    def __init__(self, client): 
        self.client = client
    
    @commands.command()
    async def shop(self, ctx):
        '''Displays the shop'''
        displayShop = discord.Embed(color = discord.Color.dark_blue(), title = "Shop")
        displayShop.add_field(name = "Lucky Amulet [$600]", value = "Increases your chances of making money during an adventure (stacks with even luckier amulet)")
        displayShop.add_field(name = "Even Luckier Amulet [$1200]", value = "Increases your chances of making money during an adventure (stacks with lucky amulet)")
        await ctx.send(embed = displayShop)
    @commands.command()
    async def buy(self, ctx, item):
        db.getItem(item)




def setup(client):
    client.add_cog(Shop(client))