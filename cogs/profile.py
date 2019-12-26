import logging

import discord
from discord.ext import commands
from collections import defaultdict
from math import floor

def calculateLevel(messageCount):
    result = 1 + messageCount/10
    if result.is_integer():
        return int(result)
    else:
        return int(floor(result))

class Profile(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.userInfo = defaultdict(lambda: defaultdict(int))

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            self.userInfo[message.author.id]["Message Count"] += 1
            if self.userInfo[message.author.id]["Level"] != calculateLevel(self.userInfo[message.author.id]["Message Count"]):
                self.userInfo[message.author.id]["Level"] = calculateLevel(self.userInfo[message.author.id]["Message Count"])
                await message.channel.send("Congratulations {}! You have reached **level {}**!".format(message.author.name, self.userInfo[message.author.id]["Level"]))

            
    @commands.command()
    async def profile(self, ctx, member: discord.Member, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        await ctx.send("**Username:** {}\n**Roles:** {}\n**Messages Sent:** {}\n **Level:** {}".format(member.display_name, ", ".join([role.name for role in member.roles[1:]]), self.userInfo[member.id]["Message Count"], self.userInfo[member.id]["Level"]))

def setup(client):
    client.add_cog(Profile(client))