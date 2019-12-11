import logging

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
client = discord.Client()

bot = commands.Bot(command_prefix="$")
botList = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command
async def hello(ctx):
    await ctx.send(ctx.message.content)

@bot.event
async def on_message(message):
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
    await bot.process_commands(message)

bot.run("NjQ0NzQ4OTYzNDU0NjQ4MzIw.Xc4nWw.mGPHYFltXUEXkwLNg7VzdJkG-WA")
