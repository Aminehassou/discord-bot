import logging
import discord
import sqlite3
import db
import datetime

from discord.ext import commands
from random import randint

class Items(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.items = {}
        self.stealCooldown = 3 * 3600
        tempItems = db.getItems()
        for item in tempItems:
            self.items[item["item_id"]] = item
    
    @commands.command()
    async def steal(self, ctx, member: discord.Member):
        if ctx.author.name == member.name:
            await ctx.send("You try to steal money from yourself... It doesn't work.")
            return 0
            
        userId = ctx.author.id
        guildId = ctx.author.guild.id
        user = db.getUser(userId, guildId)
        enemyUser = db.getUser(member.id, member.guild.id)
        lastStolen = datetime.datetime.now().timestamp()

        if user["last_stolen"] != "":
            timeSinceLastSteal = lastStolen - float(user["last_stolen"])

        else:
            timeSinceLastSteal = self.stealCooldown + 1
        
        if user["last_stolen"] != "" and timeSinceLastSteal < self.stealCooldown:
            await ctx.send("You cannot steal at this time, you must wait {:.2f} hours.".format((self.stealCooldown - timeSinceLastSteal)/3600))
            return 0
        
        if db.getUserItem(3, userId, guildId) is not None:
            if randint(1, 100) >= 50:
                moneyLost = randint(50, 150) * -1
                if enemyUser["currency"] + moneyLost < 0:
                    moneyLost = enemyUser["currency"] * -1
                db.modifyCurrency(member.id, guildId, moneyLost)
                db.modifyCurrency(userId, guildId, moneyLost * -1)
                db.updateStealTiming(userId, guildId, str(lastStolen))
                await ctx.send("You succesfully steal money from {}, you gain ${}!".format(member.name, moneyLost * -1))
            else:
                await ctx.send("You try to steal money from {}, you fail to do so.".format(member.name))
        else:
            await ctx.send("You do not own the appropriate item to use this command. Do $shop to see what items are for sale.")


def setup(client):
    client.add_cog(Items(client))