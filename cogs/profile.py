import logging

import discord
import sqlite3
import db

from discord.ext import commands
from collections import defaultdict
from collections import OrderedDict



def calculateLevel(messages):
    result = 1 + messages/10
    return int(result)
 
class Profile(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.userInfo = defaultdict(lambda: defaultdict(int))

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            currentId = message.author.id
            currentGuildId = message.author.guild.id
            print(currentGuildId)
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
        board = db.sortByMessages(10, ctx.channel.guild.id)
        output = ""
        for index, rankedUser in enumerate(board):
            output = output + "`{rank}. {name} ({count} messages)`\n".format(rank = index + 1, name = rankedUser["name"], count = rankedUser["messages"])
        await ctx.send(output)
        
def setup(client):
    client.add_cog(Profile(client))