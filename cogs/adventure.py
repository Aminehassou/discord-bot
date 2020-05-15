import logging
import discord
import sqlite3
import db
import datetime
from random import randint

from discord.ext import commands
class Adventure(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.adventureCooldown = 0.1 * 3600 #in seconds
    
    @commands.command()
    async def adventure(self, ctx):
        """Go on an adventure in order to (possibly) make money"""
        userId = ctx.author.id
        guildId = ctx.author.guild.id

        startingFailChance = 20
        endingFailChance = 30
        
        user = db.getUser(userId, guildId)
        
        luckyAmulet = db.getItem(1)
        evenLuckierAmulet = db.getItem(2)
        
        # Check if user has lucky amulet
        if db.getUserItem(luckyAmulet["item_id"], userId, guildId) is not None:
            startingFailChance -= 5
        
        # Check if user has even luckier amulet
        if db.getUserItem(evenLuckierAmulet["item_id"], userId, guildId) is not None:
            startingFailChance -= 10
            endingFailChance -= 5
        
        lastAdventured = datetime.datetime.now().timestamp()

        if user["is_upgraded"] == 0:
            await ctx.send("You must pick a class in order to be able to go on an adventure, you can pick your class at level 3")
            return 0

        if user["datetime_adventure"] != "":
            timeSinceLastAdventure = lastAdventured - float(user["datetime_adventure"])

        else:
            timeSinceLastAdventure = self.adventureCooldown + 1

        if user["datetime_adventure"] != "" and timeSinceLastAdventure < self.adventureCooldown:
            await ctx.send("You cannot adventure at this time, you must wait {:.2f} hours.".format((self.adventureCooldown - timeSinceLastAdventure)/3600))
            return 0

        db.updateAdventureTiming(userId, guildId, str(lastAdventured))
        
        for role in ctx.author.roles:
            if role.name == "Mage":
                await ctx.send("You go on a magical adventure!\nYou find a glowing rock, you decide to cast a magical spell on the rock")
                if randint(1, 100) >= randint(startingFailChance, endingFailChance):
                    await ctx.send("The rock explodes and money goes flying everywhere.\nYou gain $200!")
                    db.modifyCurrency(userId, guildId, 200)
                else:
                    await ctx.send("The rock explodes into a fiery mess, you are gravely injured, you pass out and wake up later to see the rock gone.")
                break
                
            elif role.name == "Warrior":
                await ctx.send("You go on a warrior's adventure!\nYou venture into a scary cave and find something very peculiar. It looks like a stone statue of some kind. You decide to bash the statue with your weapon")
                if randint(1, 100) >= randint(startingFailChance, endingFailChance):
                    await ctx.send("The stone statue is destroyed, you find money next to the remaining stone rubble. \nYou gain $200!")
                    db.modifyCurrency(userId, guildId, 200)
                else:
                    await ctx.send("The stone statue is actually a gargoyle statue, it shoots you with a blinding laser and you pass out. You wake up to see the statue gone.")
                break

            elif role.name == "Archer":
                await ctx.send("You go on an archer's adventure!\nYou see an object flying through the sky. You decide to shoot at it.")
                if randint(1, 100) >= randint(startingFailChance, endingFailChance):
                    await ctx.send("The flying object turned out to be a magical flying stack of cash. It flies towards you and you shoot at it again, the cash drops and you pick it up . \nYou gain $200!")
                    db.modifyCurrency(userId, guildId, 200)
                else:
                    await ctx.send("The flying object turned out to be an alien spaceship, the aliens shoot lasers at you and you pass out. You wake up to see the alien spaceship gone.")
                break
        


def setup(client):
    client.add_cog(Adventure(client))