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
        self.emotePerks = {"Damage_up": "⚔️", "Defense_up": "🛡️", "Health_up": "❤️"}


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        mssgId = payload.message_id
        if mssgId == self.roleMessage.id and payload.user_id != 644748963454648320:
            print(self.roleMessage.id)
            guildId = payload.guild_id
            guild = discord.utils.find(lambda currentGuild: currentGuild.id == guildId, self.client.guilds)
            print(payload)

            for key, value in self.emoteClasses.items():
                if payload.emoji.name == value:
                    role = discord.utils.get(guild.roles, name=key)

            for key, value in self.emotePerks.items():
                if payload.emoji.name == value:
                    role = discord.utils.get(guild.roles, name=key)
                    await self.roleMessage.delete()

            if payload.emoji.name == "4️⃣":
                    await self.roleMessage.delete()
                    role = None
            
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
    async def upgrade(self, ctx):
        """Displays currently available perks/classes"""
        currentUser = ctx.author.name
        user = db.getUser(ctx.author.id, ctx.author.guild.id)
        if user["level"] % 3 != 0:
            self.roleMessage = await ctx.send("You're not a high enough level yet!")
        
        elif user["level"] == 3:
            self.roleMessage = await ctx.send("React with one of the emotes corresponding to the class you want, {}:\n:one: : Mage\n:two: : Warrior\n:three: : Archer\n:four: : Exit".format(currentUser))
            for key, value in self.emoteClasses.items():
                await self.roleMessage.add_reaction(value)
            await self.roleMessage.add_reaction("4️⃣")

        elif user["level"] % 3 == 0 and user["level"] > 3:
            self.roleMessage = await ctx.send("React with one of the emotes corresponding to the perk you want, {}:\n⚔️ : Damage up\n🛡️ : Defense up\n❤️ : Health up".format(currentUser))
            for key, value in self.emotePerks.items():
                await self.roleMessage.add_reaction(value)

def setup(client):
    client.add_cog(Perks(client))
