import logging

import discord
from discord.ext import commands
class Profile(commands.Cog):
    def __init__(self, client): 
        self.client = client

    @commands.command()
    async def profile(self, ctx, member: discord.Member, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        counter = 0
        async for message in channel.history(limit = 200):
            if message.author == self.client.user:
                counter += 1
        await ctx.send("Username: {}\nRoles: {}\nMessages Sent: {}".format(member.display_name, (member.roles), counter))

def setup(client):
    client.add_cog(Profile(client))