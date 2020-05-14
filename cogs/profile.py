import logging

import discord

import sqlite3
import db

from discord.ext import commands
from math import sqrt


def calculateLevel(messages):
    result = 1 + (1/2)*sqrt(messages)
    return int(result)

async def hasPerk(userLevel, message, user):
    if userLevel == 3:
        await message.channel.send("{}, you've unlocked a class slot! do $upgrade to choose your class!".format(user["name"]))
        return userLevel
    elif userLevel % 3 == 0 and userLevel > 3:
        await message.channel.send("{}, you've unlocked a perk slot! do $upgrade to choose a perk!".format(user["name"]))
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
                await hasPerk(user["level"], message, user)
            db.updateUser(user)

    @commands.command()
    async def profile(self, ctx, member: discord.Member, channel: discord.TextChannel=None):
        """Displays the specified user's profile"""
        channel = channel or ctx.channel
        user = db.getUser(member.id, member.guild.id)
        if not user:
            await ctx.send("This user does not exist or has no profile information.")
            return 0

        displayProfile = discord.Embed(color = discord.Color.dark_blue(), title = "Profile")
        displayProfile.set_image(url = "{}".format(member.avatar_url))
        displayProfile.add_field(name = "**Username**", value = user["name"])
        if len(member.roles) > 1:
            displayProfile.add_field(name = "**Roles**", value = ", ".join([role.name for role in member.roles[1:]]))
        displayProfile.add_field(name = "**Messages Sent**", value = user["messages"], inline = False)
        displayProfile.add_field(name = "**Level**", value = user["level"])
        displayProfile.add_field(name = "**Currency**", value = user["currency"])
        await ctx.send(embed = displayProfile)

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