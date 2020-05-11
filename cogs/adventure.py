import logging
import discord
import sqlite3
import db
from random import randint

from discord.ext import commands
class Adventure(commands.Cog):
    def __init__(self, client): 
        self.client = client
    
    @commands.command()
    async def adventure(self, ctx):
        for role in ctx.author.roles:
            if role.name == "Mage":
                await ctx.send("You go on a magical adventure!\nYou find a glowing rock, you decide to cast a magical spell on the rock")
                if randint(1, 100) >= randint(20, 30):
                    await ctx.send("The rock explodes and you feel a surge of power!\nYou level up!")
                    user = db.getUser(ctx.author.id, ctx.author.guild.id)
                    db.updateLevel(ctx.author.id, ctx.author.guild.id, user["level"] + 1)
                else:
                    await ctx.send("The rock explodes into a fiery mess, you are gravely injured, you pass out and wake up later to see the rock gone.")
                break
                
            elif role.name == "Warrior":
                await ctx.send("You go on a warrior's adventure!")
                break

            elif role.name == "Archer":
                await ctx.send("You go on an archery adventure!")
                break



def setup(client):
    client.add_cog(Adventure(client))