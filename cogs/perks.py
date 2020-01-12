import logging

import discord
import sqlite3
import db

from discord.ext import commands
class Perks(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.roleMessage = ""
        self.emoteClasses = {"Mage": "1️⃣", "Warrior": "2️⃣", "Archer": "3️⃣"}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        mssgId = payload.message_id
        if mssgId == self.roleMessage.id:
            print(self.roleMessage.id)
            guildId = payload.guild_id
            guild = discord.utils.find(lambda currentGuild: currentGuild.id == guildId, self.client.guilds)
            print(payload)

            for key, value in self.emoteClasses.items():
                if payload.emoji.name == value:
                    role = discord.utils.get(guild.roles, name=key)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("Role successfully added!")
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        mssgId = payload.message_id
        if mssgId == self.roleMessage.id:
            guildId = payload.guild_id
            guild = discord.utils.find(lambda currentGuild: currentGuild.id == guildId, self.client.guilds)

            for key, value in self.emoteClasses.items():
                if payload.emoji.name == value:
                    role = discord.utils.get(guild.roles, name=key)
                    
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                
                if member is not None:
                    await member.remove_roles(role)
                    print("Role successfully removed!")
                else:
                    print("Member not found.")
            
            else:
                print("Role not found.")

    @commands.command()
    async def classes(self, ctx):
        """Displays currently available classes"""
        currentUser = ctx.author.name

        
        self.roleMessage = await ctx.send("React with one of the emotes corresponding to the class you want, {}:\n:one: : Mage\n:two: : Warrior\n:three: : Archer".format(currentUser))
    
    @commands.command()
    async def perks(self, ctx):
        """Displays currently available perks"""
        currentUser = ctx.author.name


        self.roleMessage = await ctx.send("React with one of the emotes corresponding to the class you want, {}:\n".format(currentUser))

def setup(client):
    client.add_cog(Perks(client))
