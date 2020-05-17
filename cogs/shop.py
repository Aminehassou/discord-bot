import logging
import discord
import sqlite3
import db
import datetime
from discord.ext import commands
class Shop(commands.Cog):
    def __init__(self, client): 
        self.client = client
    
    @commands.command()
    async def shop(self, ctx):
        '''Displays the shop'''
        displayShop = discord.Embed(color = discord.Color.dark_blue(), title = "Shop")
        displayShop.add_field(name = "1. Lucky Amulet [$600]", value = "Increases your chances of making money during an adventure (stacks with even luckier amulet)")
        displayShop.add_field(name = "2. Even Luckier Amulet [$1200]", value = "Increases your chances of making money during an adventure (stacks with lucky amulet)")
        displayShop.add_field(name = "3. Adventurer's Dagger [$900]", value = "Allows you to stab other people for a chance at stealing their money their money (unlocks the $steal command)")
        displayShop.add_field(name = "How to buy", value = "$buy [item id]")
        await ctx.send(embed = displayShop)
    @commands.command()
    async def buy(self, ctx, item):
        '''Buy an item from the shop'''
        currentItem = db.getItem(item)
        userId = ctx.author.id
        guildId = ctx.guild.id
        currentUser = db.getUser(userId, guildId)
        timeBought = datetime.datetime.now().timestamp()

        userItem = db.getUserItem(currentItem["item_id"], userId, guildId)
        
        if userItem is not None:
            await ctx.send("You already have that item, you can only own one of each item!")
            return 0
            
        if currentUser["currency"] < currentItem["item_price"]:
            await ctx.send("You do not have enough money to buy this item!")
            return 0

        db.modifyCurrency(userId, guildId, currentItem["item_price"] * -1)
        db.insertBoughtItem(currentItem["item_id"], userId, guildId, timeBought)
        await ctx.send("Succesfully bought the {}".format(currentItem["item_name"]))




def setup(client):
    client.add_cog(Shop(client))