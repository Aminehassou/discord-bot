import discord
import logging

logging.basicConfig(level=logging.INFO)
client = discord.Client()

list = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    elif message.content.startswith("$list add "):
        itemAdded = message.content[9:].strip() 
        list.append(itemAdded)
        await message.channel.send("`{}` added to list.".format(itemAdded))
    
    elif message.content.startswith("$list display"):
        if len(list) != 0:
            await message.channel.send("\n".join(["`{}. {}`".format(index + 1, anime) for index, anime in enumerate(list)]))
        else:
            await message.channel.send("The list is empty")
    
    elif message.content.startswith("$list remove "):
        try:
            indexRemoved = int(message.content[12:].strip())
        except ValueError:
            indexRemoved = -1
        
        if indexRemoved < 1 or indexRemoved > len(list):
            await message.channel.send("That element does not exist")
        else:
            itemRemoved = list.pop(indexRemoved - 1)
            await message.channel.send("Removed `{}` at index `{}`".format(itemRemoved, indexRemoved))

client.run("NjQ0NzQ4OTYzNDU0NjQ4MzIw.Xc4nWw.mGPHYFltXUEXkwLNg7VzdJkG-WA")