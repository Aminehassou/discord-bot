import logging

import discord
import sqlite3
import db

from discord.ext import commands
class Perks(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.roleMessage = ""

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        mssgId = payload.message_id
        if mssgId == self.roleMessage.id:
            print(self.roleMessage.id)
            guildId = payload.guild_id
            guild = discord.utils.find(lambda currentGuild: currentGuild.id == guildId, self.client.guilds)
            if payload.emoji.name == "one":
                role = discord.utils.get(guild.roles, name="Mage")
            elif payload.emoji.name == "two":
                role = discord.utils.get(guild.roles, name="Warrior")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
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

            if payload.emoji.name == "one":
                role = discord.utils.get(guild.roles, name="Mage")
            elif payload.emoji.name == "two":
                role = discord.utils.get(guild.roles, name="Warrior")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                
                if member is not None:
                    await member.add_removes(role)
                    print("Role successfully removed!")
                else:
                    print("Member not found.")
            
            else:
                print("Role not found.")

    @commands.command()
    async def perks(self, ctx):
        currentUser = ctx.author.name
        self.roleMessage = await ctx.send("React with one of the emotes corresponding to the perk you want, {}:\n:one: : Mage\n:two: : Warrior".format(currentUser))

def setup(client):
    client.add_cog(Perks(client))
