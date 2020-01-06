import logging

import discord
from discord.ext import commands
from collections import defaultdict
from collections import OrderedDict

def calculateLevel(messageCount):
    result = 1 + messageCount/10
    return int(result)

 
class Profile(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.userInfo = defaultdict(lambda: defaultdict(int))

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            currentId = message.author.id
            currentName = message.author.name
            newLevel = calculateLevel(self.userInfo[currentId]["messageCount"])
            self.userInfo[currentId]["messageCount"] += 1
            self.userInfo[currentId]["name"] = currentName
            if self.userInfo[currentId]["level"] != newLevel:
                self.userInfo[currentId]["level"] = newLevel
                await message.channel.send("Congratulations {}! You have reached **level {}**!".format(message.author.name, self.userInfo[currentId]["level"]))
    
    @commands.command()
    async def profile(self, ctx, member: discord.Member, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        await ctx.send("**Username:** {}\n**Roles:** {}\n**Messages Sent:** {}\n**Level:** {}".format(
            member.display_name,
            ", ".join([role.name for role in member.roles[1:]]),
            self.userInfo[member.id]["messageCount"],
            self.userInfo[member.id]["Level"])
        )
    @commands.command()
    async def leaderboard(self, ctx):
        #dict(sorted(d.items(), key = lambda x: x[1]["score"]))
        board = sorted(self.userInfo.values(), key = lambda x: x["messageCount"])[:10]
        output = ""
        for index, user in enumerate(board):
            output = output + "`{rank}. {name} ({count} messages)`\n".format(rank = index + 1, name = user["name"], count = user["messageCount"])
        await ctx.send(output)
        
def setup(client):
    client.add_cog(Profile(client))