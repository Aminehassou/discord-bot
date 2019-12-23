import logging

import discord
from discord.ext import commands
botList = []

class List(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("$list add "):
            itemAdded = message.content[9:].strip() 
            botList.append(itemAdded)
            await message.channel.send("`{}` added to list.".format(itemAdded))

        elif message.content.startswith("$list display"):
            if len(botList) != 0:
                await message.channel.send("\n".join(["`{}. {}`".format(index + 1, anime) for index, anime in enumerate(botList)]))
            else:
                await message.channel.send("The list is empty")

        elif message.content.startswith("$list remove "):
            try:
                indexRemoved = int(message.content[12:].strip())
            except ValueError:
                indexRemoved = -1
            
            if indexRemoved < 1 or indexRemoved > len(botList):
                await message.channel.send("That element does not exist")
            else:
                itemRemoved = botList.pop(indexRemoved - 1)
                await message.channel.send("Removed `{}` at index `{}`".format(itemRemoved, indexRemoved))

def setup(client):
    client.add_cog(List(client))
