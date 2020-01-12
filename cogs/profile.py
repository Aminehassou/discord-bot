import logging

import discord

import sqlite3
import db

from discord.ext import commands
from math import sqrt


def calculateLevel(messages):
    result = 1 + (1/4)*sqrt(messages)
    return int(result)

async def hasPerk(userLevel, message, user):
    if userLevel == 3:
        await message.channel.send("{}, you've unlocked a class slot! do $perks to choose your class!".format(user["name"]))
        return userLevel
    elif userLevel % 3 == 0 and userLevel > 3:
        await message.channel.send("{}, you've unlocked a class perk slot! do $perks to choose a perk!".format(user["name"]))
        return userLevel
    return None

class Profile(commands.Cog):
    def __init__(self, client): 
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            currentId = message.author.id
            currentGuildId = message.author.guild.id
            currentName = message.author.name

            user = db.getUser(currentId, currentGuildId)
            
            if not user:
                user = db.insertNewUser(currentId, currentGuildId, currentName)
            
            newLevel = calculateLevel(user["messages"])
            
            user["messages"] += 1
            user["name"] = currentName
            
            if user["level"] != newLevel:
                user["level"] = newLevel
                await message.channel.send("Congratulations {}! You have reached **level {}**!".format(user["name"], user["level"]))
            
            db.updateUser(user)

    @commands.command()
    async def profile(self, ctx, member: discord.Member, channel: discord.TextChannel=None):
        """Displays the specified user's profile"""
        channel = channel or ctx.channel
        user = db.getUser(member.id, member.guild.id)
        
        await ctx.send("**Username:** {}\n**Roles:** {}\n**Messages Sent:** {}\n**Level:** {}".format(
            user["name"],
            ", ".join([role.name for role in member.roles[1:]]),
            user["messages"],
            user["level"])
        )

    @commands.command()
    async def leaderboard(self, ctx):
        """Displays top 10 most active users by messages sent"""
        board = db.sortByMessages(10, ctx.channel.guild.id)
        output = ""
        
        for index, rankedUser in enumerate(board):
            output = output + "`{rank}. {name} ({count} messages)`\n".format(rank = index + 1, name = rankedUser["name"], count = rankedUser["messages"])
        
        await ctx.send(output)
        
def setup(client):
    client.add_cog(Profile(client))