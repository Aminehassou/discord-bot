import logging

import discord
from discord.ext import commands
class Profile(commands.Cog):
    def __init__(self, client): 
        self.client = client

    @commands.command()
    async def profile(self, ctx, member: discord.Member):
        await ctx.send(member.display_name)

def setup(client):
    client.add_cog(Profile(client))