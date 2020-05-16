import logging
import os
import discord
import config
from discord.ext import commands
logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix="$")
ownerId = 141283512345952256
@commands.command()
async def load(ctx, extension):
    if ctx.author.id == ownerId:
        client.load_extension(f"cogs.{extension}")
    else:
        await ctx.send("You are not allowed to use this command, only the bot owner can use it")

@commands.command()
async def unload(ctx, extension):
    if ctx.author.id == ownerId:
        client.unload_extension(f"cogs.{extension}")
    else:
        await ctx.send("You are not allowed to use this command, only the bot owner can use it")

@commands.command()
async def reload(ctx, extension):
    if ctx.author.id == ownerId:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
    else:
        await ctx.send("You are not allowed to use this command, only the bot owner can use it")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")    


client.run(config.TOKEN)
